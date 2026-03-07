import pandas as pd

def init_excel_db():
    db_file = "database.xlsx"
    
    # Datos iniciales (mismos que estaban quemados en app.py)
    users_data = [
        {'id': 'usuario1', 'nombre': 'Juan Pérez',    'puntos': 20000},
        {'id': 'usuario2', 'nombre': 'María García',   'puntos': 20000},
        {'id': 'usuario3', 'nombre': 'Carlos López',   'puntos': 20000}
    ]
    
    products_data = [
        {'id': 't1', 'nombre': 'iPhone 15 Pro', 'tipo': 'Tipo A (Tecnología)', 'precio': 50000, 'icono': '📱', 'descripcion': 'Pantalla Super Retina XDR de 6.1", Chip A17 Pro ultra potente y sistema de cámaras Pro.'},
        {'id': 't2', 'nombre': 'MacBook Air M2', 'tipo': 'Tipo A (Tecnología)', 'precio': 60000, 'icono': '💻', 'descripcion': 'Ultra delgada, chip M2 de Apple, pantalla Liquid Retina de 13.6" y hasta 18 horas de batería.'},
        {'id': 't3', 'nombre': 'AirPods Pro', 'tipo': 'Tipo A (Tecnología)', 'precio': 12000, 'icono': '🎧', 'descripcion': 'Cancelación Activa de Ruido, Audio Espacial personalizado y estuche de carga MagSafe.'},
        {'id': 'b1', 'nombre': 'Bono Cineco $50k', 'tipo': 'Tipo B (Bonos Digitales)', 'precio': 5000, 'icono': '🎬', 'descripcion': 'Válido para confitería o entradas en cualquier sala Cine Colombia a nivel nacional.'},
        {'id': 'b2', 'nombre': 'Bono Éxito $100k', 'tipo': 'Tipo B (Bonos Digitales)', 'precio': 10000, 'icono': '🛒', 'descripcion': 'Redimible en mercados, tecnología y hogar en almacenes Éxito y Carulla.'},
        {'id': 'b3', 'nombre': 'Bono Netflix 1 Mes', 'tipo': 'Tipo B (Bonos Digitales)', 'precio': 2500, 'icono': '📺', 'descripcion': 'Suscripción por 30 días para disfrutar de las mejores series y películas en streaming.'}
    ]
    
    config_data = [
        {'key': 'min_percentage_type_a', 'value': 50}
    ]
    
    # Crear DataFrames
    df_users = pd.DataFrame(users_data)
    df_products = pd.DataFrame(products_data)
    df_config = pd.DataFrame(config_data)
    
    # Guardar en Excel con múltiples hojas
    with pd.ExcelWriter(db_file, engine='openpyxl') as writer:
        df_users.to_excel(writer, sheet_name='Users', index=False)
        df_products.to_excel(writer, sheet_name='Products', index=False)
        df_config.to_excel(writer, sheet_name='Config', index=False)
    
    print(f"Base de datos inicializada en {db_file}")

if __name__ == "__main__":
    init_excel_db()
