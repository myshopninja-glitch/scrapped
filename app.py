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

# --- THREE.JS PHOTOREALISTIC 3D GLOBE WITH SATELLITES ---
globe_html = """
<div id="globe-container" style="width: 100%; height: 350px; display: flex; justify-content: center; align-items: center;"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
    const container = document.getElementById('globe-container');
    const scene = new THREE.Scene();
    
    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / 350, 0.1, 1000);
    camera.position.z = 320;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(container.clientWidth, 350);
    container.appendChild(renderer.domElement);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 0.6);
    dirLight.position.set(5, 3, 5);
    scene.add(dirLight);

    // 3D Earth Globe
    const geometry = new THREE.SphereGeometry(80, 64, 64);
    const textureLoader = new THREE.TextureLoader();
    
    // Photorealistic NASA Earth Map
    const earthTexture = textureLoader.load('https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/earth_atmos_2048.jpg');
    const material = new THREE.MeshPhongMaterial({
        map: earthTexture,
        shininess: 15
    });

    const earth = new THREE.Mesh(geometry, material);
    scene.add(earth);

    // Orbit 1 (Equatorial Ring & Satellite)
    const orbit1Geo = new THREE.RingGeometry(110, 111, 64);
    const orbit1Mat = new THREE.MeshBasicMaterial({ color: 0x00f2fe, side: THREE.DoubleSide, opacity: 0.4, transparent: true });
    const orbit1 = new THREE.Mesh(orbit1Geo, orbit1Mat);
    orbit1.rotation.x = Math.PI / 2.3;
    scene.add(orbit1);

    const sat1Geo = new THREE.SphereGeometry(4, 16, 16);
    const sat1Mat = new THREE.MeshBasicMaterial({ color: 0xff007f });
    const sat1 = new THREE.Mesh(sat1Geo, sat1Mat);
    scene.add(sat1);

    // Orbit 2 (Polar Ring & Satellite)
    const orbit2Geo = new THREE.RingGeometry(115, 116, 64);
    const orbit2Mat = new THREE.MeshBasicMaterial({ color: 0x00ffcc, side: THREE.DoubleSide, opacity: 0.4, transparent: true });
    const orbit2 = new THREE.Mesh(orbit2Geo, orbit2Mat);
    orbit2.rotation.y = Math.PI / 3;
    scene.add(orbit2);

    const sat2Geo = new THREE.SphereGeometry(3.5, 16, 16);
    const sat2Mat = new THREE.MeshBasicMaterial({ color: 0x00ffcc });
    scene.add(sat2Mat);
    scene.add(sat2);

    let angle1 = 0;
    let angle2 = 0;

    function animate() {
        requestAnimationFrame(animate);

        // Rotate Earth
        earth.rotation.y += 0.003;

        // Satellite 1 Positioning
        angle1 += 0.02;
        sat1.position.x = Math.cos(angle1) * 110;
        sat1.position.z = Math.sin(angle1) * 110;
        sat1.position.y = Math.sin(angle1) * 30;

        // Satellite 2 Positioning
        angle2 += 0.015;
        sat2.position.x = Math.sin(angle2) * 50;
        sat2.position.y = Math.cos(angle2) * 115;
        sat2.position.z = Math.sin(angle2) * 100;

        renderer.render(scene, camera);
    }

    animate();
</script>
"""
st.components.v1.html(globe_html, height=360)


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

    # #1 PROMINENT HERO PRODUCT
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

    # REMAINING 9 PRODUCTS (1/4 scaled size in 3x3 grid)
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
