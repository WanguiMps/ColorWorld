const videoElement = document.getElementById('video');

navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        videoElement.srcObject = stream;
    })
    .catch((error) => {
        console.error('Error accessing webcam:', error);
    });
