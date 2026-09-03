# --- REALISTIC ROTATING EARTH WITH ORBITING SATELLITES ---
globe_html = """
<div style="text-align: center; margin-bottom: 20px;">
    <canvas id="globeCanvas" width="360" height="360" style="background: transparent;"></canvas>
</div>
<script>
    const canvas = document.getElementById('globeCanvas');
    const ctx = canvas.getContext('2d');
    
    // High-resolution realistic Earth map texture
    const earthImg = new Image();
    earthImg.crossOrigin = "Anonymous";
    earthImg.src = 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Land_ocean_ice_2048.jpg/1024px-Land_ocean_ice_2048.jpg';

    let rotationOffset = 0;

    earthImg.onload = function() {
        animate();
    };

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const cx = 180, cy = 180, radius = 100;

        // 1. Draw Clip Mask for Sphere
        ctx.save();
        ctx.beginPath();
        ctx.arc(cx, cy, radius, 0, Math.PI * 2);
        ctx.clip();

        // 2. Render Rotating Earth Texture
        const imgWidth = radius * 4;
        const imgHeight = radius * 2;
        let xPos = cx - (rotationOffset % imgWidth);

        ctx.drawImage(earthImg, xPos, cy - radius, imgWidth, imgHeight);
        ctx.drawImage(earthImg, xPos + imgWidth, cy - radius, imgWidth, imgHeight);
        ctx.drawImage(earthImg, xPos - imgWidth, cy - radius, imgWidth, imgHeight);

        // 3. Realistic Atmosphere & 3D Shading Gradient
        let shadeGrad = ctx.createRadialGradient(cx - 30, cy - 30, 10, cx, cy, radius);
        shadeGrad.addColorStop(0, 'rgba(255, 255, 255, 0.1)');
        shadeGrad.addColorStop(0.7, 'rgba(0, 0, 0, 0.2)');
        shadeGrad.addColorStop(1, 'rgba(0, 5, 20, 0.85)');
        
        ctx.fillStyle = shadeGrad;
        ctx.beginPath();
        ctx.arc(cx, cy, radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        // 4. Outer Atmosphere Glow
        let glowGrad = ctx.createRadialGradient(cx, cy, radius - 2, cx, cy, radius + 12);
        glowGrad.addColorStop(0, 'rgba(0, 195, 255, 0.4)');
        glowGrad.addColorStop(1, 'rgba(0, 195, 255, 0)');
        ctx.fillStyle = glowGrad;
        ctx.beginPath();
        ctx.arc(cx, cy, radius + 12, 0, Math.PI * 2);
        ctx.fill();

        // 5. Equatorial Orbit Track & Satellite
        ctx.beginPath();
        ctx.ellipse(cx, cy, radius * 1.45, radius * 0.35, -0.2, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(0, 242, 254, 0.3)';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        let sat1X = cx + Math.cos(rotationOffset * 0.02) * (radius * 1.45);
        let sat1Y = cy + Math.sin(rotationOffset * 0.02) * (radius * 0.35);
        
        // Satellite Glow
        ctx.beginPath();
        ctx.arc(sat1X, sat1Y, 6, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 0, 128, 0.3)';
        ctx.fill();
        ctx.beginPath();
        ctx.arc(sat1X, sat1Y, 3, 0, Math.PI * 2);
        ctx.fillStyle = '#ff007f';
        ctx.fill();

        // 6. Polar Orbit Track & Satellite
        ctx.beginPath();
        ctx.ellipse(cx, cy, radius * 0.45, radius * 1.5, 0.5, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(0, 255, 204, 0.3)';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        let sat2X = cx + Math.sin(-rotationOffset * 0.015) * (radius * 0.45);
        let sat2Y = cy + Math.cos(-rotationOffset * 0.015) * (radius * 1.5);

        ctx.beginPath();
        ctx.arc(sat2X, sat2Y, 5, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(0, 255, 204, 0.3)';
        ctx.fill();
        ctx.beginPath();
        ctx.arc(sat2X, sat2Y, 2.5, 0, Math.PI * 2);
        ctx.fillStyle = '#00ffcc';
        ctx.fill();

        rotationOffset += 0.5; // Controls rotation speed
        requestAnimationFrame(animate);
    }
</script>
"""
