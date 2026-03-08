import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

# --- Configuración de la página ---
st.set_page_config(
    page_title="Alpha - Premium Rewards",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Constantes ---
DB_FILE = "database.xlsx"

# --- Estilos CSS Personalizados (Ultra-Premium) ---
def load_css():
    st.markdown("""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        
        <style>
            /* Base Modernization */
            html, body, [class*="css"], .stMarkdown, .stButton, .stText, .stHeading {
                font-family: 'Outfit', sans-serif !important;
            }
            
            h1, h2, h3 {
                font-weight: 700 !important;
                letter-spacing: -0.02em !important;
                color: #1a1a1a !important;
            }

            :root {
                --primary: #F8A71B;
                --primary-hover: #E29512;
                --bg-light: #F8F9FA;
                --text-main: #2D3436;
                --text-muted: #636E72;
                --success: #2ecc71;
                --shadow-sm: 0 2px 8px rgba(0,0,0,0.05);
                --shadow-md: 0 10px 25px rgba(0,0,0,0.08);
                --shadow-lg: 0 20px 40px rgba(0,0,0,0.12);
                --radius: 16px;
                --magic-glow: rgba(248, 167, 27, 0.4);
            }
            
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            /* Hide Streamlit's native top bar completely */
            header {visibility: hidden !important; height: 0 !important;}
            [data-testid="stHeader"] {visibility: hidden !important; height: 0 !important;}
            [data-testid="stSidebarNav"] {display: none;}
            
            .block-container {
                padding-top: 1rem !important;
                max-width: 1200px;
                padding-bottom: 5rem !important;
            }

            /* --- MAGIC UI: METEORS BACKGROUND --- */
            .meteors-container {
                position: fixed;
                top: 0; left: 0; width: 100%; height: 100%;
                z-index: -1;
                background: radial-gradient(circle at center, #1a1a1a 0%, #000 100%);
                overflow: hidden;
            }
            .meteor {
                position: absolute;
                top: 50%; left: 50%;
                width: 2px; height: 2px;
                background: linear-gradient(90deg, #fff, transparent);
                border-radius: 50%;
                transform: rotate(215deg);
                animation: meteor-animate 5s linear infinite;
            }
            .meteor::before {
                content: '';
                position: absolute;
                top: 50%; transform: translateY(-50%);
                width: 50px; height: 1px;
                background: linear-gradient(90deg, #fff, transparent);
            }
            @keyframes meteor-animate {
                0% { transform: rotate(215deg) translateX(0); opacity: 1; }
                70% { opacity: 1; }
                100% { transform: rotate(215deg) translateX(-1000px); opacity: 0; }
            }

            /* --- PRODUCT CARD (st.form wrapper) --- */
            [data-testid="stForm"] {
                background: white;
                border-radius: var(--radius) !important;
                border: 1px solid rgba(248,167,27,0.2) !important;
                box-shadow: var(--shadow-md) !important;
                padding: 8px !important;
                margin-bottom: 20px;
                transition: transform 0.15s, box-shadow 0.15s;
            }
            [data-testid="stForm"]:hover {
                transform: translateY(-2px);
                box-shadow: var(--shadow-lg) !important;
            }
            /* Remove the default Streamlit form border */
            [data-testid="stForm"] > div:first-child {
                border: none !important;
            }
            /* --- PREMIUM CARD STYLE (static card, animated border) --- */
            .magic-card {
                position: relative;
                overflow: hidden;
                border-radius: var(--radius);
                background: white;
                border: 1px solid rgba(248, 167, 27, 0.25);
                box-shadow: var(--shadow-md);
                padding: 40px;
            }
            /* The rotating pseudo-element stays BEHIND the white background */
            .magic-card::before {
                content: '';
                position: absolute;
                top: 50%; left: 50%;
                transform: translate(-50%, -50%) rotate(0deg);
                width: 150%; height: 150%;
                background: conic-gradient(
                    from 0deg,
                    transparent 0deg,
                    transparent 160deg,
                    var(--primary) 180deg,
                    transparent 200deg,
                    transparent 360deg
                );
                animation: beam-travel 4s linear infinite;
                z-index: 0;
            }
            /* White overlay sits ON TOP of the rotating element */
            .magic-card::after {
                content: '';
                position: absolute;
                inset: 2px;
                background: white;
                border-radius: calc(var(--radius) - 2px);
                z-index: 1;
            }
            /* Card content must be above the white overlay */
            .magic-card > * {
                position: relative;
                z-index: 2;
            }
            @keyframes beam-travel {
                from { transform: translate(-50%, -50%) rotate(0deg); }
                to { transform: translate(-50%, -50%) rotate(360deg); }
            }
            /* White overlay sits ON TOP of the rotating element */
            .magic-card::after {
                content: '';
                position: absolute;
                inset: 2px;
                background: white;
                border-radius: calc(var(--radius) - 2px);
                z-index: 1;
            }
            /* Card content must be above the white overlay */
            .magic-card > * {
                position: relative;
                z-index: 2;
            }
            @keyframes beam-travel {
                from { transform: translate(-50%, -50%) rotate(0deg); }
                to { transform: translate(-50%, -50%) rotate(360deg); }
            }
            /* Simpler non-animated card for admin metrics */
            .metric-card {
                background: white;
                border-radius: 20px;
                padding: 28px;
                text-align: center;
                border: 1px solid #f5f5f5;
                box-shadow: var(--shadow-md);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .metric-card:hover {
                transform: translateY(-3px);
                box-shadow: var(--shadow-lg);
            }

            /* --- MAGIC UI: SHINY BUTTON --- */
            .stButton > button, [data-testid="stFormSubmitButton"] > button {
                position: relative;
                background: var(--primary) !important;
                color: white !important;
                overflow: hidden !important;
                border: none !important;
            }
            .stButton > button::after, [data-testid="stFormSubmitButton"] > button::after {

                content: '';
                position: absolute;
                top: -50%; left: -100%;
                width: 50%; height: 200%;
                background: linear-gradient(
                    to right,
                    transparent,
                    rgba(255, 255, 255, 0.3),
                    transparent
                );
                transform: rotate(30deg);
                transition: 0s;
                pointer-events: none;
            }
            .stButton > button:hover::after, [data-testid="stFormSubmitButton"] > button:hover::after {
                left: 150%;
                transition: 0.7s;
            }

            
            /* --- GLASSMORPHISM HEADER --- */
            .fixed-header {
                position: sticky; top: 0;
                background: rgba(255, 255, 255, 0.7);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                z-index: 1000;
                padding: 12px 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.3);
                margin-bottom: 30px;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
            }
            .header-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 20px;
            }
            .balance-pill {
                background: rgba(248, 167, 27, 0.1);
                color: var(--primary);
                padding: 8px 20px;
                border-radius: 100px;
                font-weight: 700;
                border: 1px solid rgba(248, 167, 27, 0.2);
                font-size: 0.95rem;
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .product-name { font-size: 1.25rem; font-weight: 700; margin-bottom: 8px; color: #1a1a1a; }
            .product-price { color: var(--primary); font-weight: 800; font-size: 1.35rem; margin-bottom: 12px; }
            .product-description { font-size: 0.92rem; color: var(--text-muted); line-height: 1.5; min-height: 4.5em; margin-bottom: 18px; }
            
            .cart-item {
                background: white; border-radius: 12px; padding: 20px; border: 1px solid #f0f0f0; margin-bottom: 15px;
                display: flex; align-items: center; gap: 20px; box-shadow: var(--shadow-sm);
            }
            
            .checkout-card {
                background: white; border-radius: 20px; padding: 30px; border: 1px solid #f0f0f0;
                box-shadow: var(--shadow-md);
            }
            
            .step-container { display: flex; justify-content: space-between; margin-bottom: 40px; }
            .step-item { flex: 1; text-align: center; position: relative; }
            .step-circle {
                width: 36px; height: 36px; border-radius: 50%; background: #eee;
                margin: 0 auto 10px; display: flex; align-items: center; justify-content: center;
                font-weight: 700; color: #999; border: 3px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .step-circle.active { background: var(--primary); color: white; }
            .step-circle.done { background: var(--success); color: white; }
            .step-label { font-size: 0.75rem; font-weight: 700; color: #999; text-transform: uppercase; }
            
            .stTextInput > div > div > input {
                border-radius: 10px !important; border: 1.5px solid #eee !important;
                padding: 12px 15px !important; font-weight: 500 !important;
            }

            /* --- LOGIN CARD via st.container(border=True) --- */
            /* This is the real Streamlit bordered container element */
            [data-testid="stVerticalBlockBorderWrapper"] {
                position: relative !important;
                overflow: hidden !important;
                border-radius: 20px !important;
                border: none !important;
                box-shadow: 0 20px 60px rgba(0,0,0,0.10) !important;
                background: white !important;
                padding: 20px !important;
            }
            [data-testid="stVerticalBlockBorderWrapper"]::before {
                content: '';
                position: absolute;
                top: 50%; left: 50%;
                transform: translate(-50%, -50%) rotate(0deg);
                width: 150%; height: 150%;
                background: conic-gradient(
                    from 0deg,
                    transparent 0deg,
                    transparent 160deg,
                    var(--primary) 180deg,
                    transparent 200deg,
                    transparent 360deg
                );
                animation: beam-travel 4s linear infinite;
                z-index: 0;
            }
            [data-testid="stVerticalBlockBorderWrapper"]::after {
                content: '';
                position: absolute;
                inset: 3px;
                background: white;
                border-radius: 18px;
                z-index: 1;
            }
            [data-testid="stVerticalBlockBorderWrapper"] > div {
                position: relative;
                z-index: 2;
            }
            /* Product card add row */
            .product-add-row {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                margin-top: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

# --- Database Management ---
def load_db():
    if not os.path.exists(DB_FILE):
        st.error("Error: database.xlsx no encontrado. Ejecuta init_db.py")
        st.stop()
    xl = pd.ExcelFile(DB_FILE)
    users = {str(r['id']): {'nombre': r['nombre'], 'puntos': int(r['puntos'])} for _, r in xl.parse("Users").iterrows()}
    products = xl.parse("Products").to_dict('records')
    config = {r['key']: r['value'] for _, r in xl.parse("Config").iterrows()}
    return users, products, config

def save_users_to_db():
    df = pd.DataFrame([{'id': k, 'nombre': v['nombre'], 'puntos': v['puntos']} for k, v in st.session_state.users.items()])
    with pd.ExcelWriter(DB_FILE, engine='openpyxl', mode='a', if_sheet_exists='replace') as w:
        df.to_excel(w, sheet_name='Users', index=False)

def save_config_to_db():
    df = pd.DataFrame([{'key': k, 'value': v} for k, v in st.session_state.admin_settings.items()])
    with pd.ExcelWriter(DB_FILE, engine='openpyxl', mode='a', if_sheet_exists='replace') as w:
        df.to_excel(w, sheet_name='Config', index=False)

# --- Session State ---
def init_session_state():
    if 'users' not in st.session_state or 'products' not in st.session_state:
        u, p, c = load_db()
        st.session_state.users = u
        st.session_state.products = p
        st.session_state.admin_settings = c
        
    if 'current_user_id' not in st.session_state:
        st.session_state.current_user_id = None
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
    if 'navigation' not in st.session_state:
        st.session_state.navigation = "Catálogo"
    if 'checkout_step' not in st.session_state:
        st.session_state.checkout_step = 0

def get_current_user():
    return st.session_state.users.get(st.session_state.current_user_id)

# --- Cart Logic ---
def add_to_cart(product):
    st.session_state.cart.append(product)
    st.toast(f"✅ {product['nombre']} agregado")

def remove_from_cart(index):
    item = st.session_state.cart.pop(index)
    st.toast(f"❌ {item['nombre']} eliminado")

def clear_cart():
    st.session_state.cart = []

def calcular_totales_carrito():
    total_a = sum(p['precio'] for p in st.session_state.cart if "Tecnología" in p['tipo'])
    total_b = sum(p['precio'] for p in st.session_state.cart if "Bonos" in p['tipo'])
    return total_a, total_b, total_a + total_b

# --- Views ---
def show_logo(centered=True):
    """Show the real company logo from the inspiración folder."""
    import os
    logo_path = os.path.join("inspiraci\u00f3n", "Logo empresa Alpha.png")
    try:
        img = Image.open(logo_path)
        if centered:
            _, lc, _ = st.columns([1, 2, 1])
            with lc:
                st.image(img, width=180)
        else:
            st.image(img, width=140)
    except:
        st.markdown("<h2 style='color:#F8A71B;margin:0;font-weight:900;'>α ALPHA</h2>", unsafe_allow_html=True)
        st.caption("PREMIUM REWARDS")

def view_login():
    # Dark animated background
    st.markdown("""
        <div class="meteors-container">
            <div class="meteor" style="top:10%;left:80%;animation-delay:0s"></div>
            <div class="meteor" style="top:30%;left:90%;animation-delay:2s"></div>
            <div class="meteor" style="top:55%;left:70%;animation-delay:1s"></div>
            <div class="meteor" style="top:75%;left:85%;animation-delay:4s"></div>
        </div>
    """, unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
        # st.container(border=True) is the ONLY reliable way to wrap native
        # Streamlit widgets with a styled border. CSS targets stVerticalBlockBorderWrapper.
        with st.container(border=True):
            show_logo(centered=True)
            st.markdown(
                "<h3 style='margin:16px 0 4px; text-align:center;'>Bienvenido</h3>"
                "<p style='color:#888; font-size:0.92rem; margin-bottom:8px; text-align:center;'>"
                "Ingresa tu cup\u00f3n para acceder al portal.</p>",
                unsafe_allow_html=True
            )
            coupon = st.text_input("Cup\u00f3n", placeholder="X-XXXX-XXXX", label_visibility="collapsed")
            submitted = st.button("ACCEDER \u2192", use_container_width=True)
        
        if submitted:
            if not coupon:
                st.error("Ingresa un cup\u00f3n")
            elif coupon.lower() == "admin":
                st.session_state.current_user_id = "admin"
                st.session_state.is_admin = True
                st.rerun()
            else:
                uid = coupon.strip().replace(" ", "").upper()
                if uid not in st.session_state.users:
                    st.session_state.users[uid] = {'nombre': f"Usuario {uid}", 'puntos': 20000}


                    save_users_to_db()
                st.session_state.current_user_id = uid
                st.session_state.is_admin = False
                st.rerun()

def top_bar():
    """Header usando solo columnas nativas de Streamlit. Sin HTML crudo."""
    is_admin = st.session_state.is_admin
    
    c_logo, c_balance, c_btn = st.columns([2, 5, 2])
    
    with c_logo:
        show_logo(centered=False)
    
    with c_balance:
        if not is_admin:
            try:
                pts = get_current_user()["puntos"]
                st.markdown(
                    f"<div style='background:rgba(248,167,27,0.1);color:#F8A71B;padding:8px 20px;"
                    f"border-radius:100px;font-weight:700;border:1px solid rgba(248,167,27,0.3);"
                    f"font-size:0.95rem;text-align:center;margin-top:16px;'>💰 Saldo: {pts:,} pts</div>",
                    unsafe_allow_html=True
                )
            except:
                pass
        else:
            st.markdown("<div style='font-size:0.9rem;color:#888;font-weight:600;margin-top:20px;text-align:center;'>PANEL DE ADMINISTRACI\u00d3N</div>", unsafe_allow_html=True)
    
    with c_btn:
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        if st.button("Salir \u2192", key="topbar_logout", use_container_width=True):
            st.session_state.current_user_id = None
            st.session_state.navigation = "Cat\u00e1logo"
            st.session_state.checkout_step = 0
            st.rerun()
    
    st.markdown("<hr style='margin:6px 0 24px;border:none;border-top:1px solid #f0f0f0;'>", unsafe_allow_html=True)

def view_admin_dashboard():
    top_bar()
    st.subheader("Panel de Administración")
    
    u_count = len([k for k in st.session_state.users if k != "admin"])
    p_total = sum(u['puntos'] for k, u in st.session_state.users.items() if k != "admin")
    pct = st.session_state.admin_settings['min_percentage_type_a']
    
    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    for col, val, label, icon in [
        (m1, u_count, "Usuarios", "👥"),
        (m2, f"{p_total:,}", "Puntos Totales", "💰"),
        (m3, f"{pct}%", "Mín. Tecnología", "⚙️")
    ]:
        with col:
            st.markdown(f'''
                <div class="metric-card">
                    <div style="font-size:1.8rem;margin-bottom:4px;">{icon}</div>
                    <div style="font-size:2rem;font-weight:800;color:var(--primary);">{val}</div>
                    <div style="color:#888;font-size:0.78rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-top:4px;">{label}</div>
                </div>
            ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="admin-grid">', unsafe_allow_html=True)
    ca, cb = st.columns([2, 1], gap="medium")
    with ca:
        st.markdown("### 👥 Listado de Usuarios")
        df = pd.DataFrame([{'ID': k, 'Nombre': v['nombre'], 'Puntos': v['puntos']} for k, v in st.session_state.users.items() if k != "admin"])
        st.dataframe(df, use_container_width=True, hide_index=True)
    with cb:
        st.markdown("### ⚙️ Configuración")
        with st.container(border=True):
            st.markdown("<p style='font-weight: 600; margin-bottom: -15px;'>Mínimo Tecnología (%)</p>", unsafe_allow_html=True)
            new_val = st.slider("", 0, 100, int(st.session_state.admin_settings['min_percentage_type_a']))
            if new_val != st.session_state.admin_settings['min_percentage_type_a']:
                st.session_state.admin_settings['min_percentage_type_a'] = new_val
                save_config_to_db()
                st.toast("Configuración actualizada")
            st.divider()
            st.caption("Regla Bonos: 100% Puntos (Fijo)")
    
    st.markdown("### 📈 KPIs de Éxito")
    k1, k2 = st.columns(2)
    
    # KPI 1: Tasa de conversión Pago Mixto
    m_att = st.session_state.admin_settings.get('mixed_attempts', 1)
    m_suc = st.session_state.admin_settings.get('mixed_success', 0)
    conv_rate = (m_suc / m_att * 100) if m_att > 0 else 0
    
    # KPI 2: Tasa de error transaccional
    r_att = st.session_state.admin_settings.get('recovery_attempts', 1)
    r_blk = st.session_state.admin_settings.get('recovery_blocks', 0)
    err_rate = (r_blk / r_att * 100) if r_att > 0 else 0
    
    with k1:
        with st.container(border=True):
            st.markdown(f"""
                <div style="text-align:center;">
                    <div style="color:#1B5E20; font-weight:700; font-size:0.85rem; text-transform:uppercase;">Tasa de Conversión Exitosa</div>
                    <div style="font-size:2.2rem; font-weight:800; color:#2E7D32; margin:10px 0;">{conv_rate:.1f}%</div>
                    <div style="color:#888; font-size:0.75rem;">Relación de pagos mixtos efectivos vs intentados.</div>
                    <div style="margin-top:8px; color:#aaa; font-size:0.7rem;">({m_suc} éxitos / {m_att} intentos)</div>
                </div>
            """, unsafe_allow_html=True)
            
    with k2:
        with st.container(border=True):
            st.markdown(f"""
                <div style="text-align:center;">
                    <div style="color:#B71C1C; font-weight:700; font-size:0.85rem; text-transform:uppercase;">Tasa de Error Transaccional</div>
                    <div style="font-size:2.2rem; font-weight:800; color:#C62828; margin:10px 0;">{err_rate:.1f}%</div>
                    <div style="color:#888; font-size:0.75rem;">Bloqueos en recuperación de puntos vs total ejecutado.</div>
                    <div style="margin-top:8px; color:#aaa; font-size:0.7rem;">({r_blk} bloqueos / {r_att} intentos)</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def view_user_catalog():
    top_bar()
    
    # --- Sticky cart summary bar ---
    if st.session_state.cart:
        ta, tb, tt = calcular_totales_carrito()
        tt_cop = tt * 10  # 1 punto = $10 COP
        cc1, cc2, cc3 = st.columns([3, 2, 2])

        with cc1:
            st.markdown(f"<div style='background:rgba(248,167,27,0.1);border:1px solid rgba(248,167,27,0.3);border-radius:12px;padding:10px 18px;font-weight:700;color:#F8A71B;'>🛒 {len(st.session_state.cart)} producto(s) &nbsp;—&nbsp; {tt:,} pts <span style='color:#aaa;font-weight:500;font-size:0.85rem;'>≈ ${tt_cop:,} COP</span></div>", unsafe_allow_html=True)
        with cc3:
            if st.button("Ver Carrito →", use_container_width=True, type="primary"):
                st.session_state.navigation = "Carrito"
                st.rerun()
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    
    st.title("Cat\u00e1logo de Premios")
    search = st.text_input("🔍 Buscar...", placeholder="\u00bfQu\u00e9 est\u00e1s buscando?")
    t1, t2, t3 = st.tabs(["✨ Todos", "💻 Tecnolog\u00eda", "🏟\ufe0f Bonos"])
    
    cats = [None, "Tipo A (Tecnolog\u00eda)", "Tipo B (Bonos Digitales)"]
    for i, tab in enumerate([t1, t2, t3]):
        with tab:
            prods = list(st.session_state.products)
            cat_filter = cats[i]
            if cat_filter is not None:
                prods = [p for p in prods if cat_filter in str(p.get('tipo',''))]
            if search: prods = [p for p in prods if search.lower() in p['nombre'].lower()]
            
            if not prods:
                st.info("No hay productos en esta categor\u00eda.")
                continue
                
            cols = st.columns(3)
            for idx, p in enumerate(prods):
                with cols[idx % 3]:
                    peso_val = p['precio'] * 10  # 1 punto = $10 COP
                    # st.form wraps HTML + button in ONE proper DOM container

                    with st.form(key=f"prod_{i}_{idx}", border=False):
                        st.markdown(f"""
                        <div style="padding:8px;">
                            <div style="font-size:2.8rem;margin-bottom:8px;">{p['icono']}</div>
                            <div class="product-name">{p['nombre']}</div>
                            <div class="product-description">{p.get('descripcion','Detalle no disponible.')}</div>
                            <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:12px;">
                                <div>
                                    <div class="product-price" style="margin:0;">{p['precio']:,} pts</div>
                                    <div style="color:#aaa;font-size:0.8rem;">≈ ${peso_val:,} COP</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        if st.form_submit_button("A\u00f1adir \u2192", use_container_width=True, type="primary"):
                            add_to_cart(p)
                            st.rerun()



def view_cart_checkout():
    top_bar()
    
    # Progress Consolidated HTML
    steps = ["Review", "Datos", "Pago", "Éxito"]
    steps_html = '<div class="step-container">'
    for i, s in enumerate(steps):
        cls = "done" if i < st.session_state.checkout_step else ("active" if i == st.session_state.checkout_step else "")
        steps_html += f'<div class="step-item"><div class="step-circle {cls}">{"✓" if i < st.session_state.checkout_step else i+1}</div><div class="step-label {cls}">{s}</div></div>'
    steps_html += '</div>'
    st.markdown(steps_html, unsafe_allow_html=True)

    if not st.session_state.cart and st.session_state.checkout_step < 3:
        st.info("Tu carrito está vacío.")
        if st.button("Catálogo"): st.session_state.navigation = "Catálogo"; st.rerun()
        return

    # STEP 0: REVIEW
    if st.session_state.checkout_step == 0:
        c1, c2 = st.columns([1.8, 1.2], gap="large")
        with c1:
            st.markdown("### 🔍 Revisa tu selección")
            for idx, item in enumerate(st.session_state.cart):
                tipo_label = "Tecnolog\u00eda" if "Tipo A" in str(item.get('tipo', '')) else "Bono Digital"
                # Use a container with border for each item to look like a card
                with st.container(border=True):
                    ic1, ic2 = st.columns([4, 1])
                    with ic1:
                        st.markdown(f"""
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <div style="font-size: 2.2rem;">{item['icono']}</div>
                            <div>
                                <div class="product-name" style="margin:0; font-size:1.15rem;">{item['nombre']}</div>
                                <div style="color:#888; font-size:0.85rem;">{tipo_label}</div>
                                <div style="color:var(--primary); font-weight:800; font-size:1.1rem;">{item['precio']:,} pts</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    with ic2:
                        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
                        if st.button("Eliminar", key=f"del_{idx}", type="secondary", use_container_width=True):
                            remove_from_cart(idx)
                            st.rerun()

            
            st.markdown("<br>", unsafe_allow_html=True)
            col_actions = st.columns([1, 1])
            with col_actions[0]:
                if st.button("← Seguir comprando"): st.session_state.navigation = "Catálogo"; st.rerun()
            with col_actions[1]:
                if st.button("Vaciar Carrito", type="secondary"): clear_cart(); st.rerun()

        with c2:
            st.markdown("### 📋 Resumen")
            ta, tb, tt = calcular_totales_carrito()
            min_pct = st.session_state.admin_settings['min_percentage_type_a'] / 100.0
            u_pts = get_current_user()['puntos']
            req_pts = tb + (ta * min_pct)
            
            # Points currently selected (defaults to min if not selected)
            if 'final_pts_a' not in st.session_state or st.session_state.final_pts_a < int(ta*min_pct):
                st.session_state.final_pts_a = int(ta*min_pct)
            
            # THE KEY: The summary card below uses st.session_state.final_pts_a 
            # so it updates when the slider (defined later in the same script run) 
            # is moved by the user in the previous fragment of the same interaction.
            pts_to_redeem = tb + st.session_state.final_pts_a

            # Consolidated summary card — no internal type codes
            st.markdown(f"""
            <div class="checkout-card">
                <div style="display:flex; justify-content:space-between; margin-bottom:12px; color:#666;">
                    <span>Tecnología (Puntos a Redimir)</span><span>{st.session_state.final_pts_a:,} pts</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:12px; color:#666;">
                    <span>Bonos Digitales</span><span>{tb:,} pts</span>
                </div>
                <div class="summary-total" style="display:flex; justify-content:space-between; border-top: 1px dashed #eee; padding-top:15px; margin-top:15px;">
                    <span style="font-size:1.4rem;">Total a Redimir</span><span style="font-size:1.4rem; color:var(--primary);">{pts_to_redeem:,} pts</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if u_pts < req_pts:
                missing = req_pts - u_pts
                st.error(f"⚠️ Saldo insuficiente. Faltan {missing:,.0f} pts para redimir el mínimo requerido.")
                st.info(f"Tu saldo: {u_pts:,} pts | Requerido (min): {req_pts:,.0f} pts")
            else:
                st.success("✅ Puntos suficientes.")
                if ta > 0: 
                    # Selection slider for points to use on tech
                    # The slider's value is st.session_state.final_pts_a
                    st.slider(
                        "Ajustar puntos para Tecnología", 
                        int(ta*min_pct), 
                        int(min(ta, u_pts-tb)), 
                        key="final_pts_a"
                    )
                    
                    # Calculate surplus for the summary
                    exc_pts = ta - st.session_state.final_pts_a
                    exc_cop = exc_pts * 10
                    if exc_cop > 0:
                        st.warning(f"💳 Excedente a pagar: **${exc_cop:,} COP**")
                    else:
                        st.info("✨ Redención 100% con puntos.")
                else: 
                    st.session_state.final_pts_a = 0
                
                if st.button("CONTINUAR →", type="primary", use_container_width=True):
                    # Tracking KPI: Mixed payment attempt if user is NOT covering 100% with points
                    if (ta - st.session_state.final_pts_a) > 0:
                        st.session_state.admin_settings['mixed_attempts'] = st.session_state.admin_settings.get('mixed_attempts', 0) + 1
                        save_config_to_db()
                    
                    st.session_state.checkout_step = 1; st.rerun()



    # STEP 1: CONTACT
    elif st.session_state.checkout_step == 1:
        st.markdown('<div style="max-width: 500px; margin: auto;">', unsafe_allow_html=True)
        st.subheader("📍 Datos de Entrega")
        st.text_input("Email", placeholder="tu@correo.com")
        st.text_input("Nombre Completo")
        st.text_area("Dirección")
        if st.button("PAGAR →", use_container_width=True): st.session_state.checkout_step = 2; st.rerun()
        if st.button("Atrás"): st.session_state.checkout_step = 0; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # STEP 2: PAYMENT
    elif st.session_state.checkout_step == 2:
        st.markdown('<div style="max-width: 500px; margin: auto;">', unsafe_allow_html=True)
        st.subheader("💳 Pago Seguro")
        ta, tb, tt = calcular_totales_carrito()
        final_pts_a = st.session_state.get('final_pts_a', 0)
        # exc = surplus pts for tech that user does NOT cover with points
        exc_pts = ta - final_pts_a   # points not covered
        exc_cop = exc_pts * 10       # 1 punto = $10 COP
        
        if exc_pts > 0:
            st.markdown(f'''
                <div style="background: #FFF9E6; padding: 20px; border-radius: 12px; border: 1px solid #FFEBB3; margin-bottom: 25px;">
                    <div style="color: #856404; font-weight: 700; font-size: 0.9rem;">EXCEDENTE A PAGAR EN COP</div>
                    <div style="font-size: 1.8rem; font-weight: 800; color: #1a1a1a;">${exc_cop:,.0f} COP</div>
                    <div style="color:#aaa; font-size:0.82rem; margin-top:4px;">{exc_pts:,} pts × 10 = ${exc_cop:,.0f} COP</div>
                </div>
            ''', unsafe_allow_html=True)


            
            # Credit card UI using native container (no div wrappers that create floating boxes)
            with st.container(border=True):
                st.text_input("Número de Tarjeta", value="4532 0123 4567 8901")
                pc1, pc2 = st.columns(2)
                with pc1: st.text_input("Vencimiento", value="12/28")
                with pc2: st.text_input("CVV", value="123", type="password")
                st.caption("🔐 Pago encriptado de punta a punta.")
            st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.success("✅ Orden cubierta totalmente con puntos.")
            st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("CONFIRMAR ORDEN", use_container_width=True, type="primary"):
            with st.spinner("Procesando pago seguro..."):
                time.sleep(2)
                # Tracking KPI: Mixed payment success if there was an excess paid in COP
                if (ta - final_pts_a) > 0:
                    st.session_state.admin_settings['mixed_success'] = st.session_state.admin_settings.get('mixed_success', 0) + 1
                
                # Tracking KPI Recovery: Increment recovery attempts on completion
                st.session_state.admin_settings['recovery_attempts'] = st.session_state.admin_settings.get('recovery_attempts', 0) + 1
                
                st.session_state.users[st.session_state.current_user_id]['puntos'] -= (tb + st.session_state.get('final_pts_a', 0))
                save_config_to_db()
                save_users_to_db(); clear_cart(); st.session_state.checkout_step = 3; st.rerun()

        
        if st.button("Atrás"): st.session_state.checkout_step = 1; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # STEP 3: SUCCESS
    elif st.session_state.checkout_step == 3:
        st.balloons()
        st.markdown("<div style='text-align:center; padding:80px;'><h1>💎 ¡Redención Exitosa!</h1><p>Recibirás un email en breve.</p></div>", unsafe_allow_html=True)
        if st.button("Volver al Inicio"): st.session_state.navigation = "Catálogo"; st.session_state.checkout_step = 0; st.rerun()

# --- Main ---
def main():
    init_session_state()
    load_css()
    if st.session_state.current_user_id is None: view_login()
    else:
        if st.session_state.is_admin: view_admin_dashboard()
        elif st.session_state.navigation == "Catálogo": view_user_catalog()
        elif st.session_state.navigation == "Carrito": view_cart_checkout()

if __name__ == "__main__":
    main()
