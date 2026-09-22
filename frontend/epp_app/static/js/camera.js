const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureBtn = document.getElementById('captureBtn');
const resultDiv = document.getElementById('result');

const BACKEND_URL = "http://127.0.0.1:8000/api/v1/detect-epp";

// 1. Pedir acceso a la cámara al cargar la página
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        resultDiv.textContent = "No se pudo acceder a la cámara: " + err.message;
        resultDiv.className = "non-compliant";
    });

// 2. Capturar la imagen y enviarla al backend
captureBtn.addEventListener('click', () => {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append("file", blob, "capture.jpg");

        resultDiv.textContent = "Verificando...";
        resultDiv.className = "";

        fetch(BACKEND_URL, {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const helmet = data.helmet_detected ? "✅ Casco detectado" : "❌ Sin casco";
            const mask = data.mask_detected ? "✅ Tapabocas detectado" : "❌ Sin tapabocas";
            const status = data.status;

            resultDiv.innerHTML = `${helmet}<br>${mask}<br>Estado: ${status}`;
            resultDiv.className = status === "COMPLIANT" ? "compliant" : "non-compliant";
        })
        .catch(err => {
            resultDiv.textContent = "Error al conectar con el servidor: " + err.message;
            resultDiv.className = "non-compliant";
        });
    }, "image/jpeg");
});