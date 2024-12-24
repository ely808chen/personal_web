document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('signature-animation');
    const ctx = canvas.getContext('2d');

    function resizeCanvas() {
        canvas.width = canvas.clientWidth;
        canvas.height = canvas.clientHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    const text = 'Ely Chen';
    const fontSize = 40;  // Adjust font size as needed
    ctx.font = `${fontSize}px "Great Vibes", serif`;
    ctx.fillStyle = '#1c1c1c';
    ctx.fontWeight = 400;
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';

    let index = 0;
    let currentText = '';

    function drawSignature() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        currentText += text[index];
        ctx.fillText(currentText, 8, 8);  // Move text down by 5 pixels
        index++;

        if (index < text.length) {
            setTimeout(drawSignature, 500);  // Adjust speed of writing
        } else {
            setTimeout(() => {
                index = 0;
                currentText = '';
                drawSignature();
            }, 2000);  // Wait 2 seconds before restarting
        }
    }

    drawSignature();
}); 