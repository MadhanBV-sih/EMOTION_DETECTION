document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const loader = document.getElementById('loader');
    const emotionLabel = document.getElementById('emotion-label');
    const emojiDisplay = document.getElementById('emoji-display');
    const emotionCard = document.getElementById('emotion-card');
    const toggleBtn = document.getElementById('toggle-btn');
    const body = document.body;

    let isProcessing = false;
    let isPaused = false;
    let intervalId = null;

    // Smoothing Buffer
    const BUFFER_SIZE = 5;
    let emotionBuffer = [];

    // Emotion Data & Colors
    const emotionMap = {
        neutral: {
            emoji: '😐', label: 'Neutral',
            bg: 'bg-gradient-to-br from-slate-800 via-gray-800 to-slate-900',
            border: 'border-gray-500'
        },
        happy: {
            emoji: '😊', label: 'Happy',
            bg: 'bg-gradient-to-br from-yellow-500 via-orange-500 to-yellow-600',
            border: 'border-yellow-400'
        },
        sad: {
            emoji: '😔', label: 'Sad',
            bg: 'bg-gradient-to-br from-blue-600 via-indigo-600 to-blue-800',
            border: 'border-blue-400'
        },
        angry: {
            emoji: '😠', label: 'Angry',
            bg: 'bg-gradient-to-br from-red-600 via-rose-600 to-red-800',
            border: 'border-red-500'
        },
        fear: {
            emoji: '😨', label: 'Fearful',
            bg: 'bg-gradient-to-br from-purple-700 via-violet-800 to-purple-900',
            border: 'border-purple-500'
        },
        disgust: {
            emoji: '🤢', label: 'Disgusted',
            bg: 'bg-gradient-to-br from-green-600 via-emerald-700 to-green-800',
            border: 'border-green-500'
        },
        surprise: {
            emoji: '😲', label: 'Surprised',
            bg: 'bg-gradient-to-br from-pink-500 via-fuchsia-600 to-pink-700',
            border: 'border-pink-400'
        }
    };

    // Start Webcam
    async function startVideo() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;

            video.onloadedmetadata = () => {
                loader.style.display = 'none';
                startDetectionLoop();
            };
        } catch (err) {
            console.error("Camera error:", err);
            loader.innerHTML = `<p class="text-red-400">Camera Access Denied</p>`;
        }
    }

    // Detection Loop
    function startDetectionLoop() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');

        intervalId = setInterval(async () => {
            if (isProcessing || isPaused || video.paused || video.ended) return;

            isProcessing = true;

            try {
                // Capture frame
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

                const imageData = canvas.toDataURL('image/jpeg', 0.7);

                // Send to backend
                const response = await fetch('/detect_emotion', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: imageData })
                });

                if (response.status === 401) {
                    window.location.href = '/login';
                    return;
                }

                if (!response.ok) {
                    const errData = await response.json();
                    throw new Error(errData.error || 'API Error');
                }

                const data = await response.json();

                if (data.emotion) {
                    processEmotion(data.emotion, data.details);
                    // Clear error if success
                    if (loader.style.display !== 'none') {
                        loader.style.display = 'none';
                    }
                }

            } catch (err) {
                console.error("Detection error:", err);
                // Show error in loader if persistent
                if (loader.style.display === 'none') {
                    // Optional: show toast or small error indicator
                } else {
                    loader.style.display = 'block';
                    loader.innerHTML = `<p class="text-red-400 text-sm">${err.message}</p>`;
                }
            } finally {
                isProcessing = false;
            }
        }, 300); // Faster check for smoother updates
    }

    // Process Emotion with Smoothing
    function processEmotion(rawEmotion, details) {
        // Add to buffer
        emotionBuffer.push(rawEmotion);
        if (emotionBuffer.length > BUFFER_SIZE) {
            emotionBuffer.shift();
        }

        // Find most frequent emotion
        const counts = {};
        let maxCount = 0;
        let smoothEmotion = rawEmotion;

        for (const e of emotionBuffer) {
            counts[e] = (counts[e] || 0) + 1;
            if (counts[e] > maxCount) {
                maxCount = counts[e];
                smoothEmotion = e;
            }
        }

        updateUI(smoothEmotion, details);
    }

    // Update UI
    function updateUI(emotion, details) {
        const data = emotionMap[emotion] || emotionMap.neutral;

        // Update Text & Emoji
        emojiDisplay.innerText = data.emoji;
        emotionLabel.innerText = data.label;

        // Update Background Color (Smooth Transition)
        body.className = `${data.bg} min-h-screen text-white transition-colors duration-1000 ease-in-out`;

        // Update Card Border
        emotionCard.className = `glass p-8 rounded-3xl flex flex-col items-center justify-center flex-1 transition-all duration-500 border-4 ${data.border}`;
    }

    // Controls
    toggleBtn.addEventListener('click', () => {
        isPaused = !isPaused;
        toggleBtn.innerText = isPaused ? "Resume" : "Pause";
        toggleBtn.classList.toggle('bg-red-500/20', isPaused);
    });

    // Init
    startVideo();
});
