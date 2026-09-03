import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import json
import os
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(page_title="Product Trend Dashboard", layout="wide")

# Custom CSS for Tile Grids and Styling
st.markdown("""
    <style>
    .tile-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 12px;
        background-color: #ffffff;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .tile-container:hover {
        transform: translateY(-3px);
    }
    .tile-img {
        width: 100%;
        object-fit: cover;
        border-radius: 8px;
    }
    .hero-img { height: 260px; }
    .standard-img { height: 130px; }
    .platform-tag {
        font-weight: bold;
        font-size: 0.85em;
        color: #fff;
        background-color: #1f77b4;
        padding: 2px 8px;
        border-radius: 12px;
        margin-top: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Orbiting Satellite Globe Widget ---
def render_globe():
    globe_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <style>
            body { margin: 0; overflow: hidden; background-color: transparent; }
            #globe-container { width: 100%; height: 190px; }
        </style>
    </head>
    <body>
        <div id="globe-container"></div>
        <script>
            const container = document.getElementById('globe-container');
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(renderer.domElement);

            const globeGeo = new THREE.SphereGeometry(1.2, 24, 24);
            const globeMat = new THREE.MeshBasicMaterial({ color: 0x0077ff, wireframe: true });
            const globe = new THREE.Mesh(globeGeo, globeMat);
            scene.add(globe);

            const orbitGroup = new THREE.Group();
            scene.add(orbitGroup);

            for (let i = 0; i < 4; i++) {
                const satGeo = new THREE.SphereGeometry(0.06, 8, 8);
                const satMat = new THREE.MeshBasicMaterial({ color: 0xff0055 });
                const sat = new THREE.Mesh(satGeo, satMat);
                const angle = (i / 4) * Math.PI * 2;
                sat.position.set(Math.cos(angle) * 2.0, Math.sin(angle) * 0.8, Math.sin(angle) * 2.0);
                orbitGroup.add(sat);
            }

            camera.position.z = 4.5;

            function animate() {
                requestAnimationFrame(animate);
                globe.rotation.y += 0.005;
                orbitGroup.rotation.y += 0.015;
                orbitGroup.rotation.x += 0.005;
                renderer.render(scene, camera);
            }
            animate();
        </script>
    </body>
    </html>
    """
    components.html(globe_html, height=200)

# --- Header & Time Zone Display ---
header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.title("🔥 Product Trend Tracker")
    est = pytz.timezone('US/Eastern')
    current_est_time = datetime.now(est).strftime('%Y-%m-%d %I:%00 %p %Z')
    st.markdown(f"**Live Search Active** — Next scheduled update: **{current_est_time}**")

with header_col2:
    st.caption("Active Scraping Telemetry")
    render_globe()

# --- Load Data from top.py output / data.json ---
@st.cache_data(ttl=3600)
def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    else:
        # Fallback Mock Data
# Replace the mock_top_10 list inside load_data() with these valid image URLs:
mock_top_10 = [
    {"rank": 1, "name": "Wireless Headphones", "platform": "Amazon", "img_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500", "url": "https://amazon.com"},
    {"rank": 2, "name": "Sunset Lamp", "platform": "TikTok Shop", "img_url": "https://images.unsplash.com/photo-1507499739999-097706ad8914?w=500", "url": "https://tiktok.com"},
    {"rank": 3, "name": "Label Printer", "platform": "AliExpress", "img_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500", "url": "https://aliexpress.com"},
    {"rank": 4, "name": "Custom Hoodie", "platform": "Etsy", "img_url": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500", "url": "https://etsy.com"},
    {"rank": 5, "name": "Fitness Tracker", "platform": "Amazon", "img_url": "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=500", "url": "https://amazon.com"},
    {"rank": 6, "name": "Neck Massager", "platform": "TikTok Shop", "img_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=500", "url": "https://tiktok.com"},
    {"rank": 7, "name": "Desk Glow Light", "platform": "AliExpress", "img_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=500", "url": "https://aliexpress.com"},
    {"rank": 8, "name": "Leather Keychain", "platform": "Etsy", "img_url": "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=500", "url": "https://etsy.com"},
    {"rank": 9, "name": "Insulated Tumbler", "platform": "Amazon", "img_url": "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?w=500", "url": "https://amazon.com"},
    {"rank": 10, "name": "Ceramic Mug", "platform": "Etsy", "img_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500", "url": "https://etsy.com"},
]
        ]
        mock_next_15 = [
            {"Place Number": i, "Product Name": f"Up-and-Coming Item #{i}", "Source Platform": ["Amazon", "TikTok Shop", "AliExpress", "Etsy"][i % 4], "Sales Volume": 2000 - (i * 60), "Item Link": f"https://example.com/item_{i}"}
            for i in range(11, 26)
        ]
        return {"top_10": mock_top_10, "next_15": mock_next_15}

data = load_data()
top_10 = data["top_10"]
next_15 = data["next_15"]

# --- Tile Renderer ---
def render_tile(item, is_hero=False):
    img_class = "hero-img" if is_hero else "standard-img"
    title_style = "font-size: 1.15em; font-weight: bold;" if is_hero else "font-size: 0.85em;"
    
    html_code = f"""
    <div class="tile-container">
        <a href="{item['url']}" target="_blank" style="text-decoration: none; color: inherit; width: 100%;">
            <img src="{item['img_url']}" class="tile-img {img_class}" alt="{item['name']}">
            <p style="{title_style} margin: 8px 0 4px 0;">#{item['rank']} {item['name']}</p>
        </a>
        <span class="platform-tag">{item['platform']}</span>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

# --- Top 10 Centered Layout ---
st.subheader("Top 10 Selling Products")

# Row 1: Item #1 Prominently in Center
col_l, col_c, col_r = st.columns([1, 2, 1])
with col_c:
    st.markdown("### 🏆 #1 Top Seller")
    render_tile(top_10[0], is_hero=True)

# Row 2: Items #2 - #10 in 3x3 Grid
st.markdown("### Ranks #2 – #10")
grid_cols = st.columns(3)
for idx, item in enumerate(top_10[1:]):
    with grid_cols[idx % 3]:
        render_tile(item, is_hero=False)

st.divider()

# --- Next 15 Up-and-Coming List ---
st.subheader("📈 Up-and-Coming Items (Ranks 11–25)")

df_15 = pd.DataFrame(next_15)

st.dataframe(
    df_15,
    column_config={
        "Place Number": st.column_config.NumberColumn("Place #", format="#%d"),
        "Product Name": st.column_config.TextColumn("Product Name"),
        "Source Platform": st.column_config.TextColumn("Platform"),
        "Sales Volume": st.column_config.NumberColumn("Number of Sales", format="%d units"),
        "Item Link": st.column_config.LinkColumn("Purchase Link", display_text="Go to Item Page"),
    },
    hide_index=True,
    use_container_width=True
)
