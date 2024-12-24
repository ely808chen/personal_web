document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('landing-canvas');
    const ctx = canvas.getContext('2d');

    function resizeCanvas() {
        const pixelRatio = window.devicePixelRatio || 1;
        const width = window.innerWidth;
        const height = window.innerHeight;

        canvas.width = width * pixelRatio;
        canvas.height = height * pixelRatio;
        canvas.style.width = `${width}px`;
        canvas.style.height = `${height}px`;

        ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Bouncing Box
    class BouncingBox {
        constructor() {
            this.x = canvas.width / 4;
            this.y = canvas.height / 4;
            this.vx = 1.5; // Slower speed
            this.vy = 1.5; // Slower speed
            this.size = 140;
            this.hue = Math.random() * 360;
            this.texts = ["Hi", "こんにちは", "你好", "Hello", "Guten Tag", "Hola"]; // Text options
            this.textIndex = 0; // Start with "Hi"
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;

            // Correct edge collision detection
            if (this.x <= 0 || this.x + this.size >= canvas.width / window.devicePixelRatio) {
                this.vx *= -1;
                this.changeText();
                this.changeColor();
            }
            if (this.y <= 0 || this.y + this.size >= canvas.height / window.devicePixelRatio) {
                this.vy *= -1;
                this.changeText();
                this.changeColor();
            }
        }

        changeColor() {
            this.hue = Math.random() * 360;
        }

        changeText() {
            // Switch text between "Hi", "こんにちは", and "你好"
            this.textIndex = (this.textIndex + 1) % this.texts.length;
        }

        draw(ctx) {
            ctx.fillStyle = `hsl(${this.hue}, 100%, 50%)`;
            ctx.fillRect(this.x, this.y, this.size, this.size);

            ctx.fillStyle = '#fff';
            ctx.font = '28px Great Vibes';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(this.texts[this.textIndex], this.x + this.size / 2, this.y + this.size / 2);
        }
    }

    const box = new BouncingBox();

    // Neural Network Animation
    class NeuralNode {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.radius = Math.random() * 3 + 2;
            this.vx = (Math.random() - 0.5) * 0.5; // Random velocity for more fluid movement
            this.vy = (Math.random() - 0.5) * 0.5; // Random velocity
            this.alpha = Math.random() * 0.5 + 0.3;
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;

            // Simulate boundary collision with canvas edges
            if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
            if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
        }

        draw(ctx) {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(123, 216, 230, ${this.alpha})`;
            ctx.fill();
        }
    }

    class NeuralNetwork {
        constructor(nodeCount) {
            this.nodes = Array(nodeCount)
                .fill()
                .map(() => new NeuralNode());
        }

        drawConnections(ctx, box) {
            const maxDistance = 450; // Reduce max distance for more localized connections
            const boxCenterX = box.x + box.size / 2;
            const boxCenterY = box.y + box.size / 2;

            this.nodes.forEach(node => {
                const distance = Math.hypot(node.x - boxCenterX, node.y - boxCenterY);

                if (distance < maxDistance) {
                    const lineAlpha = 1 - distance / maxDistance;
                    ctx.beginPath();
                    ctx.moveTo(boxCenterX, boxCenterY);
                    ctx.lineTo(node.x, node.y);
                    ctx.strokeStyle = `rgba(173, 216, 230, ${lineAlpha})`;
                    ctx.lineWidth = 1;
                    ctx.stroke();
                }
            });
        }

        drawNodes(ctx) {
            this.nodes.forEach(node => node.draw(ctx));
        }
    }

    const neuralNetwork = new NeuralNetwork(100); // Increased nodes for better density

    // Animation loop
    function animate() {
        ctx.fillStyle = 'rgba(240, 248, 255, 0.5)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        neuralNetwork.drawConnections(ctx, box);
        neuralNetwork.drawNodes(ctx);

        box.update();
        box.draw(ctx);

        requestAnimationFrame(animate);
    }

    animate();

    // Scroll handling to make profile content visible
    const profileContent = document.querySelector('.profile-content');
    
    function checkScroll() {
        const scrollPosition = window.scrollY;
        const windowHeight = window.innerHeight;
        
        // Make profile content visible
        if (scrollPosition > windowHeight * 0.5) {
            profileContent.classList.add('visible');
        }
    }

    // Initial check in case page is loaded scrolled
    checkScroll();
    
    // Add scroll event listener
    window.addEventListener('scroll', checkScroll);
});
