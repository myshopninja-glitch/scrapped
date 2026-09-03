import base64
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

# --- CONVERT LOCAL IMAGE TO BASE64 DATA URL ---
IMAGE_PATH = "globe.png"  # Save your screenshot in the project directory as globe.png


def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""


img_base64 = get_base64_image(IMAGE_PATH)

# --- ROTATING EXACT GLOBE COMPONENT ---
if img_base64:
    globe_html = f"""
    <div style="display: flex; justify-content: center; align-items: center; width: 100%; margin: 10px 0;">
        <div class="globe-wrapper">
            <img src="data:image/png;base64,{img_base64}" class="rotating-globe">
        </div>
    </div>

    <style>
        .globe-wrapper {{
            width: 220px;
            height: 220px;
            border-radius: 50%;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 0 15px rgba(0,0,0,0.5);
        }}
        .rotating-globe {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 50%;
            animation: spin 20s linear infinite;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
    """
    st.components.v1.html(globe_html, height=250)
else:
    st.warning("Please save your globe screenshot as 'globe.png' in the root project folder.")


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
