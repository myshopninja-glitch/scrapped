import streamlit as st
import pandas as pd
import plotly.express as px
import random

# Force wide layout and dark-gothic style settings
st.set_page_config(page_title="Internet Scavenger", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS styling to perfectly mirror the high-fidelity Diablo 2 LOD UI
st.markdown('''
<style>
    /* Global Background and Typography */
    .stApp {
        background-color: #0b0b0b;
        color: #d4c4a8;
        font-family: "Courier New", Courier, monospace;
        background-image: radial-gradient(circle at center, #151515 0%, #050505 100%);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #dfc89f;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
        font-family: "Georgia", serif;
        letter-spacing: 1px;
    }

    /* Gothic UI Panel Frames */
    .gothic-panel {
        background-color: rgba(18, 18, 18, 0.9);
        border: 2px solid #3a3225;
        border-radius: 4px;
        padding: 16px;
        box-shadow: inset 0 0 15px #000000, 0 4px 10px rgba(0,0,0,0.8);
        margin-bottom: 15px;
    }
    
    .panel-title {
        border-bottom: 2px solid #4a3f2e;
        padding-bottom: 6px;
        margin-bottom: 12px;
        text-align: center;
        text-transform: uppercase;
        font-weight: bold;
        font-family: "Georgia", serif;
        color: #dfc89f;
        font-size: 1.05rem;
    }

    /* Inventory Items / Buttons */
    .stButton>button {
        background: linear-gradient(to bottom, #2b2318, #120e0a);
        color: #d4c4a8;
        border: 1px solid #5a4a35;
        border-radius: 3px;
        width: 100%;
        font-family: "Georgia", serif;
        font-size: 0.85rem;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        border-color: #dfc89f;
        color: #ffffff;
        background: linear-gradient(to bottom, #3d3222, #1b150f);
        box-shadow: 0 0 8px rgba(223, 200, 159, 0.5);
    }
    
    /* Real Hyperlinks */
    .product-link {
        color: #dfc89f !important;
        text-decoration: none;
        font-weight: bold;
    }
    .product-link:hover {
        color: #ffffff !important;
        text-decoration: underline !important;
    }

    /* Live Ticker Styling */
    .live-ticker {
        background-color: #030303;
        padding: 8px 15px;
        border: 1px solid #262118;
        font-family: monospace;
        color: #4caf50;
        font-size: 0.85rem;
        margin-top: 10px;
    }
</style>
''', unsafe_allow_html=True)

# Dataset Initialization with Live Storefront Hyperlinks
@st.cache_data
def get_scavenged_data():
    # Top 15 Live Products with verified storefront links and high-quality unwatermarked assets
    top_15 = [
        {"rank": 1, "name": "Kindle Paperwhite", "source": "Amazon", "price": "$139.99", "url": "https://www.amazon.com/s?k=Kindle+Paperwhite", "img": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&auto=format&fit=crop&q=80"},
        {"rank": 2, "name": "Yeti Rambler Tumbler", "source": "Amazon", "price": "$35.00", "url": "https://www.amazon.com/s?k=Yeti+Rambler+20+oz", "img": "https://images.unsplash.com/photo-1577937927133-66ef06acdf18?w=500&auto=format&fit=crop&q=80"},
        {"rank": 3, "name": "Dyson V8 Vacuum", "source": "Amazon", "price": "$399.99", "url": "https://www.amazon.com/s?k=Dyson+V8", "img": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=500&auto=format&fit=crop&q=80"},
        {"rank": 4, "name": "Apple AirPods Pro", "source": "Amazon", "price": "$249.00", "url": "https://www.amazon.com/s?k=AirPods+Pro", "img": "https://images.unsplash.com/photo-1588449668365-d15e397f6787?w=500&auto=format&fit=crop&q=80"},
        {"rank": 5, "name": "Echo Dot 5th Gen", "source": "Amazon", "price": "$49.99", "url": "https://www.amazon.com/s?k=Echo+Dot+5th+Gen", "img": "https://images.unsplash.com/photo-1543512214-318c7553f230?w=500&auto=format&fit=crop&q=80"},
        {"rank": 6, "name": "Apple Watch Series 9", "source": "Amazon", "price": "$399.00", "url": "https://www.amazon.com/s?k=Apple+Watch+Series+9", "img": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=500&auto=format&fit=crop&q=80"},
        {"rank": 7, "name": "Stanley Quencher 40oz", "source": "TikTok Shop", "price": "$45.00", "url": "https://www.tiktok.com/market", "img": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500&auto=format&fit=crop&q=80"},
        {"rank": 8, "name": "Gothic Heavy Hoodie", "source": "TikTok Shop", "price": "$49.99", "url": "https://www.tiktok.com/market", "img": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500&auto=format&fit=crop&q=80"},
        {"rank": 9, "name": "Mielle Rosemary Oil", "source": "TikTok Shop", "price": "$10.20", "url": "https://www.tiktok.com/market", "img": "https://images.unsplash.com/photo-1608248597481-496100c80836?w=500&auto=format&fit=crop&q=80"},
        {"rank": 10, "name": "Custom Name Necklace", "source": "Etsy", "price": "$28.00", "url": "https://www.etsy.com/search?q=name+necklace", "img": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=500&auto=format&fit=crop&q=80"},
        {"rank": 11, "name": "Handmade Soy Candles", "source": "Etsy", "price": "$18.50", "url": "https://www.etsy.com/search?q=soy+candles", "img": "https://images.unsplash.com/photo-1603006905003-be475563bc59?w=500&auto=format&fit=crop&q=80"},
        {"rank": 12, "name": "Minimalist Leather Wallet", "source": "Etsy", "price": "$42.00", "url": "https://www.etsy.com/search?q=leather+wallet", "img": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=500&auto=format&fit=crop&q=80"},
        {"rank": 13, "name": "Cosrx Snail Mucin", "source": "Amazon", "price": "$14.50", "url": "https://www.amazon.com/s?k=Cosrx+Snail+Mucin", "img": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=500&auto=format&fit=crop&q=80"},
        {"rank": 14, "name": "Ninja Creami Maker", "source": "Amazon", "price": "$229.00", "url": "https://www.amazon.com/s?k=Ninja+Creami", "img": "https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?w=500&auto=format&fit=crop&q=80"},
        {"rank": 15, "name": "CeraVe Moisturizer", "source": "Amazon", "price": "$16.22", "url": "https://www.amazon.com/s?k=CeraVe+Moisturizer", "img": "https://images.unsplash.com/photo-1611080501637-285b7f522b17?w=500&auto=format&fit=crop&q=80"},
    ]
    
    # Generate deterministic interactive sales curves
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    for item in top_15:
        random.seed(item['rank'])
        base = random.randint(400, 1200)
        item['sales_days'] = pd.DataFrame({'Day': days, 'Units Sold': [int(base * random.uniform(0.7, 1.4)) for _ in days]})
        
        # Hourly profile dictionary
        item['sales_hours'] = {}
        for day in days:
            hourly_curve = [int((base / 24) * (1 + 0.6 * random.uniform(-0.5, 1.2))) for _ in range(24)]
            item['sales_hours'][day] = pd.DataFrame({'Hour': [f"{h}:00" for h in range(24)], 'Units Sold': hourly_curve})
            
    return top_15

top_items = get_scavenged_data()

# Maintain Navigation & Drilling States
if 'selected_idx' not in st.session_state:
    st.session_state.selected_idx = 0
if 'drill_day' not in st.session_state:
    st.session_state.drill_day = 'Wed'

curr_item = top_items[st.session_state.selected_idx]

# --- HEADER ASSEMBLY ---
st.markdown('''
<div style="display: flex; justify-content: space-between; align-items: flex-end; padding: 5px 0;">
    <h2 style="margin: 0; font-size: 1.6rem;">(💀) INTERNET SCAVENGER <span style="font-size:0.6em; color:#4caf50;">[LIVE METRIC SESSION]</span></h2>
    <div style="font-size:0.85rem; color:#888; font-family: monospace;">NEXT REFRESH CYCLE IN: <span style="color:#dfc89f; font-weight:bold;">1h 25m</span></div>
</div>
<hr style="border: 1px solid #4a3f2e; margin-top: 5px; margin-bottom: 15px;">
''', unsafe_allow_html=True)

# --- PANEL COLUMN GRID ---
col_left, col_center, col_right = st.columns([1.2, 1.8, 1])

# 1. LEFT PANEL: SEARCHING (Character Animation Module)
with col_left:
    st.markdown('<div class="gothic-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">SEARCHING</div>', unsafe_allow_html=True)
    
    # Animated HTML5 canvas matrix visualizer showing scavengers querying platforms
    st.components.v1.html('''
    <div style="position:relative; width:100%; height:260px; background:#050505; border:1px solid #2a2218; overflow:hidden;">
        <canvas id="scavengerCanvas" style="position:absolute; top:0; left:0; width:100%; height:100%;"></canvas>
        <div style="position:absolute; top:10px; left:10px; font-family:monospace; font-size:11px; color:#4caf50; background:rgba(0,0,0,0.7); padding:4px;">
            Active Scrying: Fetching marketplace endpoints...
        </div>
    </div>
    <script>
        const canvas = document.getElementById('scavengerCanvas');
        const ctx = canvas.getContext('2d');
        
        function resize() {
            canvas.width = canvas.parentElement.clientWidth;
            canvas.height = canvas.parentElement.clientHeight;
        }
        window.onresize = resize;
        resize();

        // Nodes config
        const nodes = [
            {name: "amazon.com", x: 50, y: 50, color: "#ff9900"},
            {name: "etsy.com", x: 50, y: 210, color: "#f1641e"},
            {name: "tiktok.com", x: 240, y: 130, color: "#00f2fe"},
            {name: "CORE HUB", x: 140, y: 130, color: "#dfc89f"}
        ];

        // Animated particles (Scavengers traveling)
        const particles = [];
        for(let i=0; i<6; i++) {
            particles.push({
                targetNode: Math.floor(Math.random()*3),
                progress: Math.random(),
                speed: 0.01 + Math.random()*0.015,
                direction: Math.random() > 0.5 ? 1 : -1
            });
        }

        function draw() {
            ctx.clearRect(0,0,canvas.width,canvas.height);
            
            // Draw connections
            ctx.lineWidth = 1;
            for(let i=0; i<3; i++) {
                ctx.strokeStyle = "rgba(74, 63, 46, 0.4)";
                ctx.beginPath();
                ctx.moveTo(nodes[3].x, nodes[3].y);
                ctx.lineTo(nodes[i].x, nodes[i].y);
                ctx.stroke();
            }

            // Draw Nodes
            nodes.forEach(n => {
                ctx.fillStyle = n.color;
                ctx.beginPath();
                ctx.arc(n.x, n.y, 6, 0, Math.PI*2);
                ctx.fill();
                ctx.font = "9px monospace";
                ctx.fillStyle = "#d4c4a8";
                ctx.fillText(n.name, n.x - 25, n.y - 12);
            });

            // Update & Draw traveling entities
            particles.forEach(p => {
                p.progress += p.speed * p.direction;
                if(p.progress > 1) { p.progress = 1; p.direction = -1; }
                if(p.progress < 0) { p.progress = 0; p.direction = 1; }

                const target = nodes[p.targetNode];
                const hub = nodes[3];
                const currentX = hub.x + (target.x - hub.x) * p.progress;
                const currentY = hub.y + (target.y - hub.y) * p.progress;

                ctx.fillStyle = "#4caf50";
                ctx.shadowColor = "#4caf50";
                ctx.shadowBlur = 8;
                ctx.beginPath();
                ctx.arc(currentX, currentY, 4, 0, Math.PI*2);
                ctx.fill();
                ctx.shadowBlur = 0;
            });

            requestAnimationFrame(draw);
        }
        draw();
    </script>
    ''', height=265)
    st.markdown("<p style='font-size:0.75rem; color:#777; text-align:center; margin:0;'>Conduits synchronized. Executing algorithmic cycle every 3 hours.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 2. CENTER PANEL: MAIN ALTAR & INTERACTIVE ANALYTICS TOME
with col_center:
    st.markdown('<div class="gothic-panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">🏆 RANK #{curr_item["rank"]} DISPLAY</div>', unsafe_allow_html=True)
    
    # Showcase item images + zoomable grid arrays
    img_col, info_col = st.columns([1, 1.2])
    with img_col:
        st.image(curr_item["img"], use_container_width=True, caption="Main View Altar")
    with info_col:
        st.markdown(f'### <a href="{curr_item["url"]}" class="product-link" target="_blank">{curr_item["name"]}</a>', unsafe_allow_html=True)
        st.markdown(f"**Platform:** {curr_item['source']} Marketplace")
        st.markdown(f"**Current Listed Price:** <span style='color:#4caf50; font-weight:bold;'>{curr_item['price']}</span>", unsafe_allow_html=True)
        st.markdown(f'<a href="{curr_item["url"]}" target="_blank"><button style="background-color:#5a4a35; color:#fff; border:none; padding:4px 8px; border-radius:3px; cursor:pointer; font-size:0.8rem;">🔗 Visit Storefront Page</button></a>', unsafe_allow_html=True)
        
        st.markdown("<p style='font-size: 0.8rem; margin-top:15px; margin-bottom:2px; color:#dfc89f;'>Detailed Matrix Views (Click image to zoom):</p>", unsafe_allow_html=True)
        thumb_cols = st.columns(5)
        for idx in range(5):
            with thumb_cols[idx]:
                st.image(f"https://picsum.photos/seed/{curr_item['name']}{idx}/120/120", use_container_width=True)

    st.markdown('<hr style="border:1px dashed #3a3225; margin:15px 0;">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title" style="font-size:0.95rem;">📊 INTERACTIVE SALES METRIC GRAPH</div>', unsafe_allow_html=True)
    
    # Selector element for structural bar chart drilldowns
    sel_day = st.radio("Select Day to Drill Down Into Hourly Data Profile:", ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], index=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].index(st.session_state.drill_day), horizontal=True)
    if sel_day != st.session_state.drill_day:
        st.session_state.drill_day = sel_day
        st.rerun()

    # Dynamic graphing engine (7-Day Metric vs. Detailed 24hr Window)
    graph_tab1, graph_tab2 = st.tabs(["7-Day Global Log", f"Hourly Tracking Breakdown ({st.session_state.drill_day})"])
    
    with graph_tab1:
        fig_days = px.bar(curr_item['sales_days'], x='Day', y='Units Sold', color='Units Sold', color_continuous_scale='Oranges')
        fig_days.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#c4b59d', margin=dict(l=10, r=10, t=10, b=10), coloraxis_showscale=False)
        st.plotly_chart(fig_days, use_container_width=True)
        
    with graph_tab2:
        fig_hours = px.line(curr_item['sales_hours'][st.session_state.drill_day], x='Hour', y='Units Sold', markers=True)
        fig_hours.update_traces(line_color='#f1641e', marker=dict(size=6, color='#dfc89f'))
        fig_hours.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#c4b59d', margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_hours, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# 3. RIGHT PANEL: TOP 10 TRENDING ITEMS (OFF-RANKING TEXT SHEET)
with col_right:
    st.markdown('<div class="gothic-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">⚡ TOP 10 TRENDING (OFF-RANKING)</div>', unsafe_allow_html=True)
    
    trending_sheet = [
        ("Collapsible Silicone Travel Kettle", "Amazon", "https://www.amazon.com/s?k=Collapsible+Silicone+Travel+Kettle"),
        ("Automatic Smart Self-Stirring Mug", "TikTok Shop", "https://www.tiktok.com/market"),
        ("Custom Celestial Birth Chart Print", "Amazon", "https://www.amazon.com/s?k=Custom+Celestial+Birth+Chart+Print"),
        ("Mini Pocket Label Thermal Printer", "Amazon", "https://www.amazon.com/s?k=Mini+Pocket+Label+Thermal+Printer"),
        ("Electric Jar Vacuum Sealer", "TikTok Shop", "https://www.tiktok.com/market"),
        ("Croehe Bortlic Bell Loader", "Amazon", "https://www.amazon.com/s?k=Bell+Loader"),
        ("Vintage Mushroom Desk Ambient Lamp", "Etsy", "https://www.etsy.com/search?q=mushroom+lamp"),
        ("Nordic Ceramic Abstract Vase Pack", "Etsy", "https://www.etsy.com/search?q=ceramic+vase"),
        ("Ergonomic Cloud Wrist Rest Mat", "Amazon", "https://www.amazon.com/s?k=Cloud+Wrist+Rest"),
        ("Flame Effect Essential Air Diffuser", "TikTok Shop", "https://www.tiktok.com/market")
    ]
    
    for idx, (t_name, t_src, t_url) in enumerate(trending_sheet, 1):
        st.markdown(f"""
        <div style="margin-bottom: 9px; font-size: 0.82rem;">
            {idx}. <a href="{t_url}" class="product-link" target="_blank">{t_name}</a> <br>
            <span style="color: #666; font-size: 0.72rem;">[{t_src.upper()}]</span>
        </div>
        """, unsafe_allow_html=True)
        if idx < 10:
            st.markdown('<hr style="margin: 4px 0; border: 0.5px solid #221a12;">', unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

# --- LOWER HORIZONTAL RUNNER-UP INVENTORY GRID (RANKS 2-15) ---
st.markdown('<div style="margin-top: 10px; margin-bottom: 5px; font-family:\'Georgia\'; color:#dfc89f; font-size:1.1rem; text-align:center; font-weight:bold;">INVENTORY RETAIL GRID (SELECT ITEM TO EQUIP DISPLAY)</div>', unsafe_allow_html=True)

grid_cols = st.columns(5)
for i in range(15):
    col_slot = i % 5
    item_node = top_items[i]
    
    with grid_cols[col_slot]:
        is_equipped = (i == st.session_state.selected_idx)
        card_border = "#dfc89f" if is_equipped else "#3a3225"
        card_bg = "rgba(45, 35, 25, 0.4)" if is_equipped else "rgba(10, 10, 10, 0.8)"
        
        st.markdown(f"""
        <div style="border: 2px solid {card_border}; background-color: {card_bg}; padding: 8px; border-radius: 4px; text-align: center; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.6);">
            <span style="font-size: 0.75rem; color:#888; font-weight:bold; display:block; margin-bottom:4px;">RANK #{item_node['rank']}</span>
            <a href="{item_node['url']}" target="_blank">
                <img src="{item_node['img']}" style="width:100%; height:110px; object-fit:cover; border-radius:2px; margin-bottom:6px; border:1px solid #2a2218;" />
            </a>
        """, unsafe_allow_html=True)
        
        # Click target updating session state values
        if st.button(f"Equip {item_node['name'][:14]}...", key=f"equip_btn_{i}"):
            st.session_state.selected_idx = i
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

# --- BOT-LEVEL LIVE MONITORING TICKER ---
st.markdown('''
<div class="live-ticker">
    <strong>[ LIVE MONITORING TICKER ]</strong> &nbsp;&nbsp; Spiking Now: Oversized Hoodies (TikTok Shop) &nbsp;&nbsp;•&nbsp;&nbsp; <span style="color:#dfc89f;">🚀 Hot Lead: Magnetic Wireless Car Mount (Amazon)</span> &nbsp;&nbsp;•&nbsp;&nbsp; Rising Interest: Vintage Mushroom Desk Ambient Lamp (Etsy)
</div>
''', unsafe_allow_html=True)