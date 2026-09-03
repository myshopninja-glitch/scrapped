import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(
    page_title="Internet Scavenger - E-commerce Trends",
    page_icon="🛒",
    layout="wide",
)

st.title("🛒 Internet Scavenger")
st.subheader("Top Trending Products Across E-Commerce Platforms")


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
                "url": "https://amazon.com",
            },
            {
                "rank": 2,
                "name": "Sunset Lamp",
                "platform": "TikTok Shop",
                "img_url": "https://images.unsplash.com/photo-1507499739999-097706ad8914?w=500",
                "url": "https://tiktok.com",
            },
            {
                "rank": 3,
                "name": "Label Printer",
                "platform": "AliExpress",
                "img_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500",
                "url": "https://aliexpress.com",
            },
            {
                "rank": 4,
                "name": "Custom Hoodie",
                "platform": "Etsy",
                "img_url": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500",
                "url": "https://etsy.com",
            },
            {
                "rank": 5,
                "name": "Fitness Tracker",
                "platform": "Amazon",
                "img_url": "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=500",
                "url": "https://amazon.com",
            },
            {
                "rank": 6,
                "name": "Neck Massager",
                "platform": "TikTok Shop",
                "img_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=500",
                "url": "https://tiktok.com",
            },
            {
                "rank": 7,
                "name": "Desk Glow Light",
                "platform": "AliExpress",
                "img_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=500",
                "url": "https://aliexpress.com",
            },
            {
                "rank": 8,
                "name": "Leather Keychain",
                "platform": "Etsy",
                "img_url": "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=500",
                "url": "https://etsy.com",
            },
            {
                "rank": 9,
                "name": "Insulated Tumbler",
                "platform": "Amazon",
                "img_url": "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?w=500",
                "url": "https://amazon.com",
            },
            {
                "rank": 10,
                "name": "Ceramic Mug",
                "platform": "Etsy",
                "img_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500",
                "url": "https://etsy.com",
            },
        ]
        mock_next_15 = [
            {
                "Place Number": i,
                "Product Name": f"Up-and-Coming Item #{i}",
                "Source Platform": [
                    "Amazon",
                    "TikTok Shop",
                    "AliExpress",
                    "Etsy",
                ][i % 4],
                "Sales Volume": 2000 - (i * 60),
                "Item Link": f"https://example.com/item_{i}",
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
        st.image(item["img_url"], use_container_width=True)
        st.markdown(f"**#{item['rank']} {item['name']}**")
        st.caption(f"Platform: {item['platform']}")
        st.markdown(f"[View Product]({item['url']})")

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
