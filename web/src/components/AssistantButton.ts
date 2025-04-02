import apiRoutes from "../apiRoutes";
import { qs } from "../selectors";
import { ComponentProps } from "../types";
import { insertElement } from "../utils";


export default (props: ComponentProps): Element | undefined => {
  const assistantButtonHTML = `
    <section class="assistant-container">
      <h1 class="sr-only">AI Voice Assistant</h1>
      <div id="conversation-history" class="conversation-history" aria-live="polite"></div>
      <div id="response" class="response" aria-live="polite"></div>
      <button id="circle" class="circle" aria-label="Hold to talk to AI assistant">
        <span class="circle-text">Hold to Talk</span>
        <svg class="microphone-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
          <line x1="12" y1="19" x2="12" y2="23"></line>
          <line x1="8" y1="23" x2="16" y2="23"></line>
        </svg>
        <canvas id="waveform" class="waveform"></canvas>
      </button>
      <div id="loading" class="loading" aria-hidden="true">
        <div class="spinner"></div>
      </div>
    </section>
`

  insertElement({ parent: props.parent, child: assistantButtonHTML, position: "beforeend" });

  type AudioState = 'idle' | 'recording' | 'processing' | 'playing';

  interface AIResponse {
    transcription: string,
    response: string,
    audio: Blob
  }

  // DOM Elements
  const circle = qs('#circle')! as HTMLButtonElement;
  const circleText = qs('.circle-text')! as HTMLSpanElement;
  const response = qs('#response')! as HTMLDivElement;
  const conversationHistory = qs('#conversation-history')! as HTMLDivElement;
  const loading = qs('#loading')! as HTMLDivElement;
  const canvas = qs('#waveform')! as HTMLCanvasElement;
  const canvasCtx = canvas.getContext('2d')!;

  // State
  let mediaRecorder: MediaRecorder | null = null;
  let audioChunks: Blob[] = [];
  let isRecording = false;
  let audioContext: AudioContext | null = null;
  let analyser: AnalyserNode | null = null;
  let dataArray: Uint8Array | null = null;
  let currentState: AudioState = "idle"
  let audioPlayer: HTMLAudioElement | null = null;

  // Event Listeners
  function initializeEventListeners(): void {
    circle.addEventListener('mousedown', handleCircleInteraction);
    circle.addEventListener('mouseup', handleCircleInteraction);
    circle.addEventListener('mouseleave', handleCircleInteraction);
    circle.addEventListener('touchstart', handleCircleInteraction);
    circle.addEventListener('touchend', handleCircleInteraction);
    document.addEventListener('keydown', handleKeyPress);
    document.addEventListener('keyup', handleKeyPress);
  }

  function handleCircleInteraction(event: Event): void {
    if (currentState === 'idle' && (event.type === 'mousedown' || event.type === 'touchstart')) {
      startRecording(event);
    } else if (currentState === 'recording' && (event.type === 'mouseup' || event.type === 'mouseleave' || event.type === 'touchend')) {
      stopRecording(event);
    }
  }

  function handleKeyPress(event: KeyboardEvent): void {
    if (event.code === 'Space') {
      event.preventDefault();
      if (event.type === 'keydown' && currentState === 'idle') {
        startRecording(event);
      } else if (event.type === 'keyup' && currentState === 'recording') {
        stopRecording(event);
      }
    }
  }

  // Recording Functions
  async function startRecording(event: Event): Promise<void> {
    event.preventDefault();
    if (currentState !== 'idle') return;
    currentState = 'recording';
    isRecording = true;
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      audioChunks = [];

      mediaRecorder.addEventListener('dataavailable', (event: BlobEvent) => {
        audioChunks.push(event.data);
      });

      mediaRecorder.start();
      updateCircleState('recording');

      audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      analyser = audioContext.createAnalyser();
      const microphone = audioContext.createMediaStreamSource(stream);
      microphone.connect(analyser);
      analyser.fftSize = 256;
      dataArray = new Uint8Array(analyser.frequencyBinCount);
      drawWaveform();

    } catch (error) {
      console.error('Error accessing microphone:', error);
      displayResponse('Error accessing microphone. Please check your permissions.');
      currentState = 'idle';
    }
  }

  function stopRecording(event: Event): void {
    event.preventDefault();
    if (currentState !== 'recording') return;
    isRecording = false;
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop();
      mediaRecorder.addEventListener('stop', processAudio);
      updateCircleState('processing');
      currentState = 'processing';
    }
    if (audioContext) {
      audioContext.close();
    }
    canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
  }

  function drawWaveform(): void {
    if (!analyser || !dataArray) return;

    canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
    analyser.getByteTimeDomainData(dataArray);
    canvasCtx.lineWidth = 2;
    canvasCtx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
    canvasCtx.beginPath();

    const sliceWidth = canvas.width * 1.0 / dataArray.length;
    let x = 0;

    for (let i = 0; i < dataArray.length; i++) {
      const v = dataArray[i] / 128.0;
      const y = v * canvas.height / 2;

      if (i === 0) {
        canvasCtx.moveTo(x, y);
      } else {
        canvasCtx.lineTo(x, y);
      }

      x += sliceWidth;
    }

    canvasCtx.lineTo(canvas.width, canvas.height / 2);
    canvasCtx.stroke();

    if (isRecording) {
      requestAnimationFrame(drawWaveform);
    }
  }

  // Audio Processing
  async function processAudio(): Promise<void> {
    showLoading();
    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');

    try {
      const response = await fetch(apiRoutes.TALK_ASSISTANT, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result: AIResponse = await response.json();
        console.log(result)
        addConversationItem(result.transcription, 'user-message');
        displayResponse(result.response);
        addConversationItem(result.response, 'ai-message');
        // if (result.audio) {
        //   playAudioResponse(result.audio);
        // }
      } else {
        throw new Error('Failed to process audio');
      }
    } catch (error) {
      console.error('Error processing audio:', error);
      displayResponse('Sorry, there was an error processing your request.');
      currentState = 'idle';
    }

    updateCircleState('idle');
    hideLoading();
  }

  // Audio Playback
  function playAudioResponse(audio: Blob): void {
    if (audioPlayer) {
      audioPlayer.pause();
      audioPlayer = null;
    }

    const audioUrl = URL.createObjectURL(audio);
    audioPlayer = new Audio(audioUrl);
    audioPlayer.addEventListener('ended', () => {
      currentState = 'idle';
      updateCircleState('idle');
    });

    audioPlayer.addEventListener('error', () => {
      console.error('Error playing audio response');
      currentState = 'idle';
      updateCircleState('idle');
    });

    audioPlayer.play();
    currentState = 'playing';
    updateCircleState('playing');
  }

  // UI Updates
  function displayResponse(text: string): void {
    response.textContent = text;
    response.style.opacity = '1';
    setTimeout(() => {
      response.style.opacity = '0';
    }, 5000);
  }

  function updateCircleState(state: AudioState): void {
    switch (state) {
      case 'recording':
        circleText.textContent = 'Recording...';
        circle.style.backgroundColor = '#e74c3c';
        break;
      case 'processing':
        circleText.textContent = 'Processing...';
        circle.style.backgroundColor = '#f39c12';
        break;
      case 'playing':
        circleText.textContent = 'Playing...';
        circle.style.backgroundColor = '#2ecc71';
        break;
      case 'idle':
      default:
        circleText.textContent = 'Hold to Talk';
        circle.style.backgroundColor = '';
        break;
    }
  }

  function addConversationItem(text: string, className: string): void {
    const item = document.createElement('div');
    item.className = `conversation-item ${className}`;
    item.textContent = text;
    conversationHistory.appendChild(item);
    conversationHistory.scrollTop = conversationHistory.scrollHeight;
  }

  function showLoading(): void {
    loading.style.display = 'block';
  }

  function hideLoading(): void {
    loading.style.display = 'none';
  }

  initializeEventListeners();
};

