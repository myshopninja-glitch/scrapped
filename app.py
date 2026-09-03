import json
import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Internet Scavenger - E-commerce Trends",
    page_icon="🛒",
    layout="wide",
)

st.title("🛒 Internet Scavenger")
st.subheader("Top Trending Products Across Amazon and Etsy")

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

        rotationOffset += 0.5;
        requestAnimationFrame(animate);
    }
</script>
"""
st.components.v1.html(globe_html, height=350)


@st.cache_data(ttl=3600)
def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    else:
        mock_top_10 = [
            {
                "rank": 1,
                "name": "Wireless Headphones",
                "platform": "Amazon",
                "img_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800",
                "url": "https://www.amazon.com/s?k=wireless+headphones",
            },
            {
                "rank": 2,
                "name": "Custom Embroidered Hoodie",
                "platform": "Etsy",
                "img_url": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=400",
                "url": "https://www.etsy.com/search?q=custom+embroidered+hoodie",
            },
            {
                "rank": 3,
                "name": "Smart Fitness Band",
                "platform": "Amazon",
                "img_url": "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400",
                "url": "https://www.amazon.com/s?k=smart+fitness+tracker",
            },
            {
                "rank": 4,
                "name": "Personalized Keychain",
                "platform": "Etsy",
                "img_url": "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=400",
                "url": "https://www.etsy.com/search?q=personalized+leather+keychain",
            },
            {
                "rank": 5,
                "name": "Stainless Tumbler",
                "platform": "Amazon",
                "img_url": "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?w=400",
                "url": "https://www.amazon.com/s?k=stainless+steel+tumbler",
            },
            {
                "rank": 6,
                "name": "Handmade Ceramic Mug",
                "platform": "Etsy",
                "img_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=400",
                "url": "https://www.etsy.com/search?q=handmade+ceramic+mug",
            },
            {
                "rank": 7,
                "name": "Bluetooth Speaker",
                "platform": "Amazon",
                "img_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400",
                "url": "https://www.amazon.com/s?k=bluetooth+speaker",
            },
            {
                "rank": 8,
                "name": "Handmade Soy Candle",
                "platform": "Etsy",
                "img_url": "https://images.unsplash.com/photo-1603006905003-be475563bc59?w=400",
                "url": "https://www.etsy.com/search?q=handmade+soy+candle",
            },
            {
                "rank": 9,
                "name": "Ergonomic Desk Mat",
                "platform": "Amazon",
                "img_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400",
                "url": "https://www.amazon.com/s?k=desk+pad+mat",
            },
            {
                "rank": 10,
                "name": "Customized Tote Bag",
                "platform": "Etsy",
                "img_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=400",
                "url": "https://www.etsy.com/search?q=customized+tote+bag",
            },
        ]
        mock_next_15 = [
            {
                "Place Number": i,
                "Product Name": f"Up-and-Coming Item #{i}",
                "Source Platform": ["Amazon", "Etsy"][i % 2],
                "Sales Volume": 2400 - (i * 75),
                "Item Link": f"https://www.amazon.com/s?k=trending+item+{i}"
                if i % 2 == 0
                else f"https://www.etsy.com/search?q=trending+item+{i}",
            }
            for i in range(11, 26)
        ]
        return {"top_10": mock_top_10, "next_15": mock_next_15}


data = load_data()
top_10 = data.get("top_10", [])

st.header("🔥 Top 10 Hot Products")

if top_10:
    left_col, right_col = st.columns([2.5, 3])

    # #1 PROMINENT HERO ITEM
    with left_col:
        item_1 = top_10[0]
        st.markdown("### 🏆 #1 Top Trending")
        hero_html = f"""
        <a href="{item_1['url']}" target="_blank" style="text-decoration:none; color:inherit;">
            <div style="border: 2px solid #FFD700; border-radius:15px; padding: 12px; background: rgba(255, 215, 0, 0.05); text-align:center;">
                <img src="{item_1['img_url']}" style="width:100%; height:440px; object-fit:cover; border-radius:10px; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                <h2 style="margin: 12px 0 4px 0;">#1 {item_1['name']}</h2>
                <p style="color:#aaa; margin:0;">Platform: <b>{item_1['platform']}</b></p>
            </div>
        </a>
        """
        st.markdown(hero_html, unsafe_allow_html=True)

    # REMAINING 9 ITEMS (1/4 scaled size in 3x3 grid)
    with right_col:
        st.markdown("### ⚡ Trending Runners-Up")
        grid_items = top_10[1:10]

        for row in range(3):
            cols = st.columns(3)
            for col_idx in range(3):
                item_idx = row * 3 + col_idx
                if item_idx < len(grid_items):
                    item = grid_items[item_idx]
                    with cols[col_idx]:
                        thumb_html = f"""
                        <a href="{item['url']}" target="_blank" style="text-decoration:none; color:inherit;">
                            <div style="border: 1px solid #333; border-radius:8px; padding: 6px; text-align:center; margin-bottom:10px;">
                                <img src="{item['img_url']}" style="width:100%; height:110px; object-fit:cover; border-radius:6px; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.04)'" onmouseout="this.style.transform='scale(1)'">
                                <div style="font-size:0.8rem; font-weight:bold; margin-top:4px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">#{item['rank']} {item['name']}</div>
                                <div style="font-size:0.7rem; color:#888;">{item['platform']}</div>
                            </div>
                        </a>
                        """
                        st.markdown(thumb_html, unsafe_allow_html=True)

st.markdown("---")
st.header("📈 Next 15 Rising Trends")

if "next_15" in data and data["next_15"]:
    df = pd.DataFrame(data["next_15"])
    st.dataframe(
        df,
        column_config={
            "Item Link": st.column_config.LinkColumn("Product Link")
        },
        use_container_width=True,
        hide_index=True,
    )
