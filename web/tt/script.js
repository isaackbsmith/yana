class AIAssistant {
    constructor() {
        this.circle = document.getElementById('circle');
        this.response = document.getElementById('response');
        this.circleText = this.circle.querySelector('.circle-text');
        this.conversationHistory = document.getElementById('conversation-history');
        this.loading = document.getElementById('loading');
        this.canvas = document.getElementById('waveform');
        this.canvasCtx = this.canvas.getContext('2d');
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.circle.addEventListener('mousedown', this.startRecording.bind(this));
        this.circle.addEventListener('mouseup', this.stopRecording.bind(this));
        this.circle.addEventListener('mouseleave', this.stopRecording.bind(this));
        this.circle.addEventListener('touchstart', this.startRecording.bind(this));
        this.circle.addEventListener('touchend', this.stopRecording.bind(this));
        document.addEventListener('keydown', this.handleKeyPress.bind(this));
        document.addEventListener('keyup', this.handleKeyPress.bind(this));
    }

    handleKeyPress(event) {
        if (event.code === 'Space') {
            event.preventDefault();
            if (event.type === 'keydown' && !this.isRecording) {
                this.startRecording(event);
            } else if (event.type === 'keyup' && this.isRecording) {
                this.stopRecording(event);
            }
        }
    }

    async startRecording(event) {
        event.preventDefault();
        if (this.isRecording) return;
        this.isRecording = true;
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];

            this.mediaRecorder.addEventListener('dataavailable', (event) => {
                this.audioChunks.push(event.data);
            });

            this.mediaRecorder.start();
            this.updateCircleState('recording');

            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.analyser = this.audioContext.createAnalyser();
            this.microphone = this.audioContext.createMediaStreamSource(stream);
            this.microphone.connect(this.analyser);
            this.analyser.fftSize = 256;
            this.dataArray = new Uint8Array(this.analyser.frequencyBinCount);
            this.drawWaveform();

            this.addConversationItem('Listening...', 'user-message');
        } catch (error) {
            console.error('Error accessing microphone:', error);
            this.displayResponse('Error accessing microphone. Please check your permissions.');
        }
    }

    stopRecording(event) {
        event.preventDefault();
        if (!this.isRecording) return;
        this.isRecording = false;
        if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
            this.mediaRecorder.stop();
            this.mediaRecorder.addEventListener('stop', this.processAudio.bind(this));
            this.updateCircleState('processing');
        }
        if (this.audioContext) {
            this.audioContext.close();
        }
        this.canvasCtx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }

    drawWaveform() {
        this.canvasCtx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.analyser.getByteTimeDomainData(this.dataArray);
        this.canvasCtx.lineWidth = 2;
        this.canvasCtx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
        this.canvasCtx.beginPath();

        const sliceWidth = this.canvas.width * 1.0 / this.dataArray.length;
        let x = 0;

        for (let i = 0; i < this.dataArray.length; i++) {
            const v = this.dataArray[i] / 128.0;
            const y = v * this.canvas.height / 2;

            if (i === 0) {
                this.canvasCtx.moveTo(x, y);
            } else {
                this.canvasCtx.lineTo(x, y);
            }

            x += sliceWidth;
        }

        this.canvasCtx.lineTo(this.canvas.width, this.canvas.height / 2);
        this.canvasCtx.stroke();

        if (this.isRecording) {
            requestAnimationFrame(this.drawWaveform.bind(this));
        }
    }

    async processAudio() {
        this.showLoading();
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.wav');

        try {
            const response = await fetch('http://your-fastapi-backend-url/process-audio', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const result = await response.json();
                this.displayResponse(result.text);
                this.addConversationItem(result.text, 'ai-message');
            } else {
                throw new Error('Failed to process audio');
            }
        } catch (error) {
            console.error('Error processing audio:', error);
            this.displayResponse('Sorry, there was an error processing your request.');
        }

        this.updateCircleState('idle');
        this.hideLoading();
    }

    displayResponse(text) {
        this.response.textContent = text;
        this.response.style.opacity = '
