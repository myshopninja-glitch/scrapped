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

# --- GUARANTEED SVG VECTOR GLOBE (NO CORS / NO EXTERNAL TEXTURE DEPENDENCY) ---
globe_html = """
<div style="display: flex; justify-content: center; align-items: center; width: 100%; margin: 10px 0;">
    <div style="position: relative; width: 260px; height: 260px; display: flex; justify-content: center; align-items: center;">
        
        <!-- SVG Vector Globe -->
        <svg viewBox="0 0 200 200" style="width: 200px; height: 200px; filter: drop-shadow(0px 0px 15px rgba(0, 195, 255, 0.4));">
            <defs>
                <radialGradient id="oceanGrad" cx="30%" cy="30%" r="70%">
                    <stop offset="0%" stop-color="#1e3c72" />
                    <stop offset="100%" stop-color="#0a1128" />
                </radialGradient>
                <clipPath id="globeClip">
                    <circle cx="100" cy="100" r="95" />
                </clipPath>
            </defs>
            
            <!-- Sphere Base -->
            <circle cx="100" cy="100" r="95" fill="url(#oceanGrad)" stroke="#00f2fe" stroke-width="1.5"/>
            
            <!-- Rotating Map Landmasses -->
            <g clip-path="url(#globeClip)">
                <g class="spin-continents" fill="#20bf6b" opacity="0.85">
                    <!-- Continents Group 1 -->
                    <path d="M 30 50 Q 50 30 70 60 T 90 110 T 50 140 T 20 90 Z" />
                    <path d="M 120 40 Q 150 20 170 50 T 160 100 T 130 80 Z" />
                    <path d="M 110 120 Q 140 110 150 150 T 120 170 Z" />
                    <!-- Continents Group 2 (Repeated for seamless loop) -->
                    <path d="M 230 50 Q 250 30 270 60 T 290 110 T 250 140 T 220 90 Z" />
                    <path d="M 320 40 Q 350 20 370 50 T 360 100 T 330 80 Z" />
                    <path d="M 310 120 Q 340 110 350 150 T 320 170 Z" />
                </g>
                <!-- Grid Lines -->
                <circle cx="100" cy="100" r="95" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
                <ellipse cx="100" cy="100" rx="95" ry="35" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
                <ellipse cx="100" cy="100" rx="95" ry="70" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
                <line x1="100" y1="5" x2="100" y2="195" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
            </g>
        </svg>

        <!-- Equatorial Orbit & Satellite -->
        <div class="orbit-eq">
            <div class="sat-1"></div>
        </div>

        <!-- Polar Orbit & Satellite -->
        <div class="orbit-pol">
            <div class="sat-2"></div>
        </div>
    </div>
</div>

<style>
    .spin-continents {
        animation: rotateMap 18s linear infinite;
    }
    @keyframes rotateMap {
        0% { transform: translateX(0px); }
        100% { transform: translateX(-200px); }
    }

    .orbit-eq {
        position: absolute;
        width: 250px;
        height: 70px;
        border: 1.5px solid rgba(0, 242, 254, 0.5);
        border-radius: 50%;
        transform: rotate(-20deg);
        animation: orbitSpin1 5s linear infinite;
    }
    .sat-1 {
        position: absolute;
        top: -5px;
        left: 50%;
        width: 10px;
        height: 10px;
        background: #ff007f;
        border-radius: 50%;
        box-shadow: 0 0 8px #ff007f;
    }

    .orbit-pol {
        position: absolute;
        width: 70px;
        height: 250px;
        border: 1.5px solid rgba(0, 255, 204, 0.5);
        border-radius: 50%;
        transform: rotate(30deg);
        animation: orbitSpin2 7s linear infinite;
    }
    .sat-2 {
        position: absolute;
        top: 50%;
        left: -5px;
        width: 9px;
        height: 9px;
        background: #00ffcc;
        border-radius: 50%;
        box-shadow: 0 0 8px #00ffcc;
    }

    @keyframes orbitSpin1 {
        0% { transform: rotate(-20deg) rotate(0deg); }
        100% { transform: rotate(-20deg) rotate(360deg); }
    }
    @keyframes orbitSpin2 {
        0% { transform: rotate(30deg) rotate(0deg); }
        100% { transform: rotate(30deg) rotate(360deg); }
    }
</style>
"""
st.components.v1.html(globe_html, height=280)


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
