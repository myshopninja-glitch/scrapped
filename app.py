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
                "img_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500",
                "url": "https://www.amazon.com/s?k=wireless+headphones",
            },
            {
                "rank": 2,
                "name": "Custom Embroidered Hoodie",
                "platform": "Etsy",
                "img_url": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500",
                "url": "https://www.etsy.com/search?q=custom+embroidered+hoodie",
            },
            {
                "rank": 3,
                "name": "Fitness Tracker",
                "platform": "Amazon",
                "img_url": "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=500",
                "url": "https://www.amazon.com/s?k=smart+fitness+tracker",
            },
            {
                "rank": 4,
                "name": "Personalized Leather Keychain",
                "platform": "Etsy",
                "img_url": "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=500",
                "url": "https://www.etsy.com/search?q=personalized+leather+keychain",
            },
            {
                "rank": 5,
                "name": "Insulated Stainless Tumbler",
                "platform": "Amazon",
                "img_url": "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?w=500",
                "url": "https://www.amazon.com/s?k=stainless+steel+tumbler",
            },
            {
                "rank": 6,
                "name": "Aesthetic Handmade Mug",
                "platform": "Etsy",
                "img_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500",
                "url": "https://www.etsy.com/search?q=handmade+ceramic+mug",
            },
            {
                "rank": 7,
                "name": "Bluetooth Portable Speaker",
                "platform": "Amazon",
                "img_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500",
                "url": "https://www.amazon.com/s?k=bluetooth+speaker",
            },
            {
                "rank": 8,
                "name": "Handmade Soy Candle",
                "platform": "Etsy",
                "img_url": "https://images.unsplash.com/photo-1603006905003-be475563bc59?w=500",
                "url": "https://www.etsy.com/search?q=handmade+soy+candle",
            },
            {
                "rank": 9,
                "name": "Ergonomic Desk Mat",
                "platform": "Amazon",
                "img_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500",
                "url": "https://www.amazon.com/s?k=desk+pad+mat",
            },
            {
                "rank": 10,
                "name": "Customized Tote Bag",
                "platform": "Etsy",
                "img_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=500",
                "url": "https://www.etsy.com/search?q=customized+tote+bag",
            },
        ]
        mock_next_15 = [
            {
                "Place Number": i,
                "Product Name": f"Up-and-Coming Item #{i}",
                "Source Platform": ["Amazon", "Etsy"][i % 2],
                "Sales Volume": 2000 - (i * 60),
                "Item Link": f"https://www.amazon.com/s?k=trending+product+{i}"
                if i % 2 == 0
                else f"https://www.etsy.com/search?q=trending+product+{i}",
            }
            for i in range(11, 26)
        ]
        return {"top_10": mock_top_10, "next_15": mock_next_15}


data = load_data()

st.header("🔥 Top 10 Hot Products")
cols = st.columns(5)

for idx, item in enumerate(data.get("top_10", [])):
    col = cols[idx % 5]
    with col:
        clickable_image = f"""
        <a href="{item['url']}" target="_blank">
            <img src="{item['img_url']}" style="width:100%; border-radius:10px; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
        </a>
        """
        st.markdown(clickable_image, unsafe_allow_html=True)
        st.markdown(f"**#{item['rank']} {item['name']}**")
        st.caption(f"Platform: {item['platform']}")

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
