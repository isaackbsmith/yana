import os
import numpy as np
import soundfile as sf
import librosa
from pathlib import Path
from typing import Annotated
from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException

from yana.assistant.request_handler import handle_request
from yana.domain.exceptions import ServiceError
from yana.api.exceptions import InternalServerError
from yana.api.types import Config
from yana.domain.models.assistant import AudioResponseModel
from yana.utils.config import get_config
from yana.lib.speech_recognizer import SpeechRecogizer
from yana.lib.intent_recognizer import IntentRecognizer
from yana.lib.entity_recognizer import NamedEntityRecognizer


router = APIRouter(prefix="/assistant", tags=["assistant"])

@router.get("/")
async def home() -> str:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="This endpoint is not allowed"
    )

UPLOAD_PATH = Path("yana/static/audio/web.wav")
RESPONSE_PATH = Path("yana/static/audio/response.wav")
config = get_config()
stt = SpeechRecogizer(config)
ir = IntentRecognizer(config)
ner = NamedEntityRecognizer(config)

@router.post("/talk")
async def process_audio(audio: Annotated[UploadFile, File(description="User audio")]):
    try:
        # Read the audio file data
        audio_data = await audio.read()

        # Save the uploaded file temporarily
        temp_file_path = Path("yana/static/audio/tmp.wav")
        with open(temp_file_path, "wb") as f:
            f.write(audio_data)

        # Load the audio file using librosa
        y, sr = librosa.load(temp_file_path, sr=None)  # Keep original sampling rate

        # Resample the audio to 16kHz
        y_resampled = librosa.resample(y, orig_sr=sr, target_sr=16000)

        # Normalize to avoid clipping
        y_resampled = y_resampled / np.max(np.abs(y_resampled))

        # Convert to 16-bit PCM format
        y_resampled_16bit = np.int16(y_resampled * 32767)

        # Save the processed audio to a new file
        sf.write(UPLOAD_PATH, y_resampled_16bit, samplerate=16000, subtype='PCM_16')

        # Optionally, clean up the temporary file
        os.remove(temp_file_path)

        # Transcribe
        transcription = stt.recognize_web(UPLOAD_PATH)

        if transcription:
            intent = ir.recognize([transcription])
            entities = ner.recognize(transcription)
            response = await handle_request(config, intent, entities, web=True)
            if response:
                return {
                        "transcription": transcription,
                        "response": response.response,
                        "audio": FileResponse(RESPONSE_PATH, media_type="audio/wav", filename="response.wav")
                }
        else:
            return AudioResponseModel(transcription="...", response=None, audio=None)
    except Exception as e:
        print("Audio Error: ", e)
        raise HTTPException(status_code=500, detail=f"An error occurred")
