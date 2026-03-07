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
            header [data-testid="stAppDeploy"] {display: none;}
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

            /* --- MAGIC UI: BORDER BEAM (Robust Version) --- */
            .magic-card {
                position: relative;
                padding: 4px;
                border-radius: var(--radius);
                background: #f0f0f0; /* Fallback */
                background: conic-gradient(from 0deg, transparent, transparent, var(--primary));
                animation: rotate-beam 4s linear infinite;
                box-shadow: var(--shadow-md);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            .magic-inner {
                background: white;
                border-radius: calc(var(--radius) - 4px);
                padding: 40px;
                width: 100%;
                height: 100%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            @keyframes rotate-beam {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }

            /* --- MAGIC UI: SHINY BUTTON --- */
            .stButton > button {
                position: relative;
                background: var(--primary) !important;
                overflow: hidden !important;
                border: none !important;
            }
            .stButton > button::after {
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
            .stButton > button:hover::after {
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

            /* --- ADMIN BENTO --- */
            .admin-grid {
                display: grid;
                grid-template-columns: 2fr 1fr;
                gap: 25px;
            }
            .metric-card-magic {
                position: relative;
                padding: 30px;
                background: white;
                border-radius: 24px;
                text-align: center;
                border: 1px solid #f0f0f0;
                overflow: hidden;
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
def show_logo():
    try:
        img = Image.open("logo_alpha.png")
        st.image(img, width=180)
    except:
        st.markdown("<h1 style='color: #F8A71B; margin: 0;'>ALPHA</h1>", unsafe_allow_html=True)
        st.caption("PREMIUM REWARDS")

def view_login():
    # Inject Meteors Background
    st.markdown("""
        <div class="meteors-container">
            <div class="meteor" style="top: 10%; left: 80%; animation-delay: 0s;"></div>
            <div class="meteor" style="top: 30%; left: 90%; animation-delay: 2s;"></div>
            <div class="meteor" style="top: 50%; left: 70%; animation-delay: 1s;"></div>
            <div class="meteor" style="top: 70%; left: 85%; animation-delay: 4s;"></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Grid for centering
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        
        # ONE SINGLE CONTAINER for everything
        st.markdown('<div class="magic-card"><div class="magic-inner">', unsafe_allow_html=True)
        
        show_logo()
        st.markdown("<br><h3 style='margin-bottom:0;'>Bienvenido</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #888; font-size:0.92rem; margin-bottom:25px;'>Ingresa tu cupón para acceder al portal.</p>", unsafe_allow_html=True)
        
        coupon = st.text_input("Cupón", placeholder="X-XXXX-XXXX", label_visibility="collapsed")
        
        st.markdown("<div style='margin-top:15px;'>", unsafe_allow_html=True)
        submit_btn = st.button("ACCEDER →", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if coupon or submit_btn:
            if submit_btn and not coupon:
                st.error("Ingresa un cupón")
            elif coupon:
                if coupon.lower() == "admin":
                    st.session_state.current_user_id = "admin"
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    uid = coupon.strip().replace(" ", "").upper()
                    if uid not in st.session_state.users:
                        st.session_state.users[uid] = {'nombre': f"Usuario {uid}", 'puntos': 15000}
                        save_users_to_db()
                    st.session_state.current_user_id = uid
                    st.session_state.is_admin = False
                    st.rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)

def top_bar():
    is_admin = st.session_state.is_admin
    user_title = "ADMIN" if is_admin else "ALPHA"
    
    balance_pill = ""
    if not is_admin:
        try:
            pts = get_current_user()["puntos"]
            balance_pill = f'<div class="balance-pill">💰 Saldo: {pts:,} pts</div>'
        except:
            balance_pill = ""

    # Clean header HTML - Zero stray divs
    st.markdown(f'''
        <div class="fixed-header">
            <div class="header-container">
                <div style="font-size: 1.5rem; font-weight: 800; letter-spacing: -1px; color: #1a1a1a;">{user_title}</div>
                {balance_pill}
                <div style="width: 120px;"></div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Position SALIR button correctly using a cleaner overlay strategy
    st.markdown("<div style='position: relative; top: -72px; height: 0; z-index: 1001;'>", unsafe_allow_html=True)
    c1, c2 = st.columns([9.5, 1.5])
    with c2:
        if st.button("SALIR", key="global_logout_final_v4"):
            st.session_state.current_user_id = None
            st.session_state.navigation = "Catálogo"
            st.session_state.checkout_step = 0
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def view_admin_dashboard():
    top_bar()
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2>Panel de Administración 💠</h2>", unsafe_allow_html=True)
    
    u_count = len([k for k in st.session_state.users if k != "admin"])
    p_total = sum(u['puntos'] for k, u in st.session_state.users.items() if k != "admin")
    
    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    for col, val, label in [(m1, u_count, "Usuarios"), (m2, f"{p_total:,}", "Puntos Totales"), (m3, f"{st.session_state.admin_settings['min_percentage_type_a']}%", "Mín. Tecnología")]:
        with col:
            st.markdown(f'''
                <div class="magic-card" style="padding: 24px; text-align: center; border: 1px solid #f0f0f0;">
                    <div style="font-size: 2.2rem; font-weight: 800; color: var(--primary);">{val}</div>
                    <div style="color: #888; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-top: 5px;">{label}</div>
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
    st.markdown('</div>', unsafe_allow_html=True)

def view_user_catalog():
    top_bar()
    st.title("Catálogo de Premios")
    
    search = st.text_input("🔍 Buscar...", placeholder="¿Qué estás buscando?")
    t1, t2, t3 = st.tabs(["✨ Todos", "💻 Tecnología", "🎟️ Bonos"])
    
    cats = [None, "Tecnología (Tipo A)", "Bonos Digitales (Tipo B)"]
    for i, tab in enumerate([t1, t2, t3]):
        with tab:
            prods = st.session_state.products
            if cats[i]: prods = [p for p in prods if p['tipo'] == cats[i]]
            if search: prods = [p for p in prods if search.lower() in p['nombre'].lower()]
            
            if not prods: st.info("No hay productos."); continue
                
            cols = st.columns(3)
            for idx, p in enumerate(prods):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div class="magic-card" style="padding: 24px; margin-bottom: 20px;">
                        <div style="font-size: 3rem; margin-bottom: 10px;">{p['icono']}</div>
                        <div class="product-name">{p['nombre']}</div>
                        <div class="product-description">{p.get('descripcion', 'Detalle no disponible.')}</div>
                        <div class="product-price">{p['precio']:,} pts</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Añadir →", key=f"add_{i}_{idx}"): add_to_cart(p)
    
    if st.session_state.cart:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"VER CARRITO ({len(st.session_state.cart)}) 🛒", type="primary", use_container_width=True):
            st.session_state.navigation = "Carrito"
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
                # Using columns for the item and the remove button to avoid manual div breaking
                with st.container():
                    st.markdown(f"""
                    <div class="cart-item">
                        <div style="font-size: 2.2rem;">{item['icono']}</div>
                        <div style="flex-grow: 1;">
                            <div class="product-name" style="margin:0; font-size:1.15rem;">{item['nombre']}</div>
                            <div style="color:#888; font-size:0.85rem;">{item['tipo']}</div>
                        </div>
                        <div style="color:var(--primary); font-weight:800; font-size:1.2rem; margin-right:15px;">{item['precio']:,} pts</div>
                    </div>
                    """, unsafe_allow_html=True)
                    # Use unique column logic for the button interaction
                    bt_c1, bt_c2 = st.columns([10, 2])
                    with bt_c2:
                        if st.button("Eliminar", key=f"del_{idx}"):
                            remove_from_cart(idx); st.rerun()
            
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
            
            # Consolidated summary card
            st.markdown(f"""
            <div class="checkout-card">
                <div style="display:flex; justify-content:space-between; margin-bottom:12px; color:#666;">
                    <span>Tecnología (Tipo A)</span><span>{ta:,} pts</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:12px; color:#666;">
                    <span>Bonos (Tipo B)</span><span>{tb:,} pts</span>
                </div>
                <div class="summary-total" style="display:flex; justify-content:space-between; border-top: 1px dashed #eee; padding-top:15px; margin-top:15px;">
                    <span style="font-size:1.4rem;">Total</span><span style="font-size:1.4rem;">{tt:,} pts</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            req_pts = tb + (ta * min_pct)
            
            if u_pts < req_pts: 
                st.error(f"Faltan {(req_pts-u_pts):,.0f} pts para redimir.")
            else:
                st.success("✅ Puntos suficientes.")
                if ta > 0: 
                    st.session_state.final_pts_a = st.slider("Puntos para Tecnología", int(ta*min_pct), int(min(ta, u_pts-tb)), int(ta*min_pct))
                else: 
                    st.session_state.final_pts_a = 0
                
                if st.button("CONTINUAR →", type="primary", use_container_width=True):
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
        exc = ta - st.session_state.get('final_pts_a', 0)
        
        if exc > 0:
            st.markdown(f'''
                <div style="background: #FFF9E6; padding: 20px; border-radius: 12px; border: 1px solid #FFEBB3; margin-bottom: 25px;">
                    <div style="color: #856404; font-weight: 700; font-size: 0.9rem;">EXCEDENTE A PAGAR</div>
                    <div style="font-size: 1.8rem; font-weight: 800; color: #1a1a1a;">${exc:,.0f} COP</div>
                </div>
            ''', unsafe_allow_html=True)
            
            # Simulated Card UI
            st.markdown("<div style='background: white; padding: 25px; border-radius: 20px; border: 1px solid #eee; box-shadow: var(--shadow-md);'>", unsafe_allow_html=True)
            st.text_input("Número de Tarjeta", value="4532 0123 4567 8901")
            pc1, pc2 = st.columns(2)
            with pc1: st.text_input("Vencimiento", value="12/28")
            with pc2: st.text_input("CVV", value="123", type="password")
            st.caption("🔐 Pago encriptado de punta a punta.")
            st.markdown("</div><br>", unsafe_allow_html=True)
        else:
            st.success("✅ Orden cubierta totalmente con puntos.")
            st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("CONFIRMAR ORDEN", use_container_width=True, type="primary"):
            with st.spinner("Procesando pago seguro..."):
                time.sleep(2)
                st.session_state.users[st.session_state.current_user_id]['puntos'] -= (tb + st.session_state.get('final_pts_a', 0))
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
