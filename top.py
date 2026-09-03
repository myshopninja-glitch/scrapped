import streamlit as st
import pandas as pd
import plotly.express as px
import random

# Page configuration
st.set_page_config(page_title="Internet Scavenger", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for Diablo 2 LOD Gothic/Dark Fantasy Theme
st.markdown('''
<style>
    /* Global Styles */
    .stApp {
        background-color: #0d0d0d;
        color: #d4c4a8;
        font-family: "Courier New", Courier, monospace;
        background-image: radial-gradient(circle at center, #1a1a1a 0%, #000000 100%);
    }
    
    h1, h2, h3, h4, h5 {
        color: #dfc89f;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        font-family: "Georgia", serif;
        letter-spacing: 1px;
    }

    /* Panel/Container Borders simulating gothic frames */
    .metric-box {
        background-color: rgba(20, 20, 20, 0.85);
        border: 2px solid #3d3a33;
        border-radius: 8px;
        padding: 15px;
        box-shadow: inset 0 0 20px #000, 0 0 10px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    
    .panel-header {
        border-bottom: 1px solid #4a4233;
        padding-bottom: 10px;
        margin-bottom: 15px;
        text-align: center;
        text-transform: uppercase;
        font-weight: bold;
    }

    /* Button Styling */
    .stButton>button {
        background: linear-gradient(to bottom, #2a2a2a, #111111);
        color: #d4c4a8;
        border: 1px solid #5a5040;
        border-radius: 4px;
        width: 100%;
        transition: all 0.2s ease-in-out;
        font-family: serif;
    }
    .stButton>button:hover {
        border-color: #dfc89f;
        color: #ffffff;
        background: linear-gradient(to bottom, #3a3a3a, #1a1a1a);
        box-shadow: 0 0 8px rgba(223, 200, 159, 0.4);
    }
    
    /* Links */
    a {
        color: #a89f91;
        text-decoration: none;
        transition: color 0.3s;
    }
    a:hover {
        color: #dfc89f;
        text-decoration: underline;
    }

    /* Ticker */
    .ticker {
        background-color: #050505;
        padding: 10px;
        border-top: 1px solid #222;
        border-bottom: 1px solid #222;
        font-family: monospace;
        color: #4caf50;
        font-size: 0.9em;
        white-space: nowrap;
        overflow: hidden;
    }
</style>
''', unsafe_allow_html=True)

# Generate Mock Data
@st.cache_data
def load_data():
    items = [
        {"id": 0, "name": "Kindle Paperwhite", "source": "Amazon", "price": "$139.99"},
        {"id": 1, "name": "Yeti Rambler 20oz", "source": "Amazon", "price": "$35.00"},
        {"id": 2, "name": "Dyson V8 Absolute", "source": "Amazon", "price": "$399.99"},
        {"id": 3, "name": "Apple AirPods Pro", "source": "Amazon", "price": "$249.00"},
        {"id": 4, "name": "Echo Dot (5th Gen)", "source": "Amazon", "price": "$49.99"},
        {"id": 5, "name": "Apple Watch Series 9", "source": "Amazon", "price": "$399.00"},
        {"id": 6, "name": "Stanley Quencher", "source": "TikTok Shop", "price": "$45.00"},
        {"id": 7, "name": "Vintage Hoodie", "source": "TikTok Shop", "price": "$29.99"},
        {"id": 8, "name": "Mielle Scalp Oil", "source": "TikTok Shop", "price": "$18.50"},
        {"id": 9, "name": "Name Necklace", "source": "Etsy", "price": "$24.00"},
        {"id": 10, "name": "Soy Candle Set", "source": "Etsy", "price": "$22.00"},
        {"id": 11, "name": "Leather Wallet", "source": "Etsy", "price": "$45.00"},
        {"id": 12, "name": "Cosrx Snail Mucin", "source": "Amazon", "price": "$15.00"},
        {"id": 13, "name": "Ninja Creami", "source": "Amazon", "price": "$199.99"},
        {"id": 14, "name": "CeraVe Cream", "source": "Amazon", "price": "$17.99"},
    ]
    
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    for item in items:
        base_sales = random.randint(300, 1500)
        item['sales'] = pd.DataFrame({
            'Day': days,
            'Units Sold': [int(base_sales * random.uniform(0.7, 1.4)) for _ in days]
        })
    return items

items = load_data()

# Manage Session State for Selected Item
if 'selected_idx' not in st.session_state:
    st.session_state.selected_idx = 0

selected_item = items[st.session_state.selected_idx]

# Top Header Layout
st.markdown('''
<div style="display: flex; justify-content: space-between; align-items: flex-end; padding: 10px 0;">
    <h2 style="margin: 0;">(💀) INTERNET SCAVENGER <span style="font-size:0.5em; color:#4caf50;">[LIVE METRIC SESSION]</span></h2>
    <div style="font-size:0.9em; color:#888;">NEXT REFRESH CYCLE IN: <span style="color:#dfc89f;">1h 25m</span></div>
</div>
<hr style="border: 1px solid #3d3d3d; margin-top: 0;">
''', unsafe_allow_html=True)

# --- 3 COLUMN MAIN LAYOUT ---
col1, col2, col3 = st.columns([1.2, 1.8, 1])

# Left Column: Search Visualizer
with col1:
    st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-header'>SEARCHING</div>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1633356122544-f134324a6cee?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", caption="Active Scrying: Processing top sellers...")
    st.markdown("<p style='font-size: 0.8em; color: #888; text-align: center;'>[ Nodes Connected: Amazon, Etsy, TikTok ]<br>Decrypting logic gates... Data Acquired.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Center Column: Main Altar & Graph
with col2:
    st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
    st.markdown(f"<div class='panel-header'>🏆 RANK #{st.session_state.selected_idx + 1} DISPLAY</div>", unsafe_allow_html=True)
    
    # Selected Item Display
    subcol1, subcol2 = st.columns([1, 1.2])
    with subcol1:
        st.image(f"https://picsum.photos/seed/{selected_item['name'].replace(' ', '')}/400/500", use_column_width=True)
    with subcol2:
        st.markdown(f"### **Product:** [{selected_item['name']}](#)")
        st.markdown(f"<span style='color:#888;'>Source: {selected_item['source']} Marketplace</span><br>", unsafe_allow_html=True)
        st.markdown(f"**Est. Price:** {selected_item['price']}")
        
        st.markdown("<br><p style='font-size: 0.8em; margin-bottom: 5px;'>Detailed Views (Click to zoom):</p>", unsafe_allow_html=True)
        t_cols = st.columns(5)
        for i in range(5):
            with t_cols[i]:
                st.image(f"https://picsum.photos/seed/{selected_item['name'].replace(' ', '')}{i}/150/150", use_column_width=True)
    
    st.markdown("<hr style='border: 1px solid #333;'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-header' style='font-size:1em;'>📊 SALES METRIC GRAPH</div>", unsafe_allow_html=True)
    
    # Interactive Graph
    fig = px.bar(selected_item['sales'], x='Day', y='Units Sold', 
                 color='Units Sold', color_continuous_scale='Oranges')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#c4b59d',
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="",
        yaxis_title="Units",
        coloraxis_showscale=False,
        hovermode="x"
    )
    fig.update_traces(marker_line_width=1, marker_line_color="#4a4233")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("<p style='text-align:center; font-size:0.75em; color:#888;'>(Hover/Click bar for daily breakdown; current selection: [Hour Curve])</p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Right Column: Trending List
with col3:
    st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-header'>⚡ TOP 10 TRENDING ITEMS<br><span style='font-size:0.7em; color:#888;'>(OFF-RANKING)</span></div>", unsafe_allow_html=True)
    
    trends = [
        ("Custom Engraved Moon Phase Lamp", "ETSY"),
        ("Smart Reusable Notebook", "AMAZON"),
        ("Mushroom Coffee Starter Kit", "TIKTOK"),
        ("Portable Fabric Shaver", "AMAZON"),
        ("Silicone Wine Glass Holder", "ETSY"),
        ("Cold Brew Coffee Maker", "TIKTOK"),
        ("Magnetic Wireless Car Mount", "AMAZON"),
        ("Retro Gaming Consoles", "ETSY"),
        ("Heated Desk Pad", "AMAZON"),
        ("Crystal Hair Eraser", "TIKTOK")
    ]
    
    for t_name, t_source in trends:
        st.markdown(f"<a href='#'><b>{t_name}</b> <span style='font-size:0.8em; color:#666;'>[{t_source}]</span></a>", unsafe_allow_html=True)
        st.markdown("<hr style='margin: 0.4em 0; border: 0.5px solid #222;'>", unsafe_allow_html=True)
        
    st.markdown("<p style='font-size:0.75em; color:#888; margin-top:15px; text-align:justify;'>Note: These items have high velocity but haven't reached Top 15 sales volume yet.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- BOTTOM INVENTORY GRID ---
st.markdown("<h4 style='text-align: center; margin-top: 20px; color: #dfc89f;'>Inventory Grid (Select to Equip View)</h4>", unsafe_allow_html=True)

grid_container = st.container()
with grid_container:
    cols = st.columns(7)
    for i in range(15):
        col_idx = i % 7
        with cols[col_idx]:
            border_color = "#dfc89f" if i == st.session_state.selected_idx else "#3d3a33"
            bg_color = "rgba(40,30,20,0.8)" if i == st.session_state.selected_idx else "rgba(20,20,20,0.8)"
            
            st.markdown(f"<div style='border: 2px solid {border_color}; background-color: {bg_color}; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 15px;'>", unsafe_allow_html=True)
            st.image(f"https://picsum.photos/seed/{items[i]['name'].replace(' ', '')}/150/150")
            
            if st.button(f"#{i+1} {items[i]['name'][:12]}", key=f"btn_{i}"):
                st.session_state.selected_idx = i
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# Bottom Ticker
st.markdown("<br><div class='ticker'>[ LIVE MONITORING TICKER ] &nbsp;&nbsp;&nbsp; Spiking Now: Oversized Hoodies (TikTok)... &nbsp;&nbsp;&nbsp; 🚀 Hot Lead: Magnetic Wireless Car Mount (AliExpress)... &nbsp;&nbsp;&nbsp; Rising Interest: Retro Gaming Consoles (Etsy)...</div>", unsafe_allow_html=True)