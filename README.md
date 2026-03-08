# 💠 Alpha Premium Rewards

> Portal de redención de puntos y bonos digitales para empleados y clientes corporativos.

---

## 🚀 Instalación rápida

```bash
pip install -r requirements.txt
python init_db.py        # Solo la primera vez
streamlit run app.py
```

Disponible en `http://localhost:8501`

---

## 🔐 Acceso

| Perfil | Cupón | Puntos iniciales |
|--------|-------|-----------------|
| **Administrador** | `admin` | — |
| **Usuario** | Cualquier código (ej. `JUAN-001`) | **20,000 pts** |

---

## 💱 Conversión de puntos

```
1 punto = $10 COP
```

Ejemplo: 50,000 pts → **$500,000 COP**


---

## 🛒 Lógica del carrito — Descripción detallada

Este es el núcleo del sistema. El carrito maneja **dos tipos de productos con reglas distintas de pago** y un flujo de 4 pasos.

### Diagrama de implementación

![Diagrama del carrito](inspiraci%C3%B3n/diagrama%20implementacio%CC%81n%20carrito.png)

---

### Tipos de productos y sus reglas

| Tipo | Código interno | Regla de pago |
|------|----------------|---------------|
| **Tecnología** | `Tipo A (Tecnología)` | Se puede pagar con puntos entre un **mínimo** y el **100%** del precio. El excedente (puntos faltantes) se cobra en **COP** a la tasa 1 pt = $10 COP. |

| **Bonos Digitales** | `Tipo B (Bonos Digitales)` | Siempre se pagan **100% en puntos**. Sin pago adicional. |

El mínimo de puntos para Tecnología lo configura el administrador (por defecto **50%**). Si se fija en 70%, el usuario debe cubrir al menos el 70% del precio en puntos; el resto puede pagarlo en COP.

---

### Cálculo de totales

```python
total_tipo_a = suma de precios de productos Tecnología en el carrito
total_tipo_b = suma de precios de productos Bonos en el carrito

puntos_minimos_requeridos = total_tipo_b + (total_tipo_a × min_porcentaje)
```

Si `puntos_usuario < puntos_minimos_requeridos` → el usuario **no puede proceder** al checkout y se muestra el déficit exacto en puntos.

---

### Flujo paso a paso

```
[Catálogo] → [Carrito] → [Datos de entrega] → [Pago] → [Confirmación]
  Step 0       Step 0         Step 1            Step 2      Step 3
```

#### Step 0 — Carrito

- Lista todos los ítems con su tipo y precio.
- Calcula `total_a`, `total_b` y `total_general`.
- Muestra el resumen de puntos **disponibles vs. requeridos**.
- Muestra el **Excedente a pagar en COP** basado en la selección del slider (si aplica).
- Si hay puntos suficientes, aparece un **slider** para elegir cuántos puntos destinar a Tecnología:
  - Mínimo: `total_a × min_porcentaje`
  - Máximo: `min(total_a, puntos_disponibles − total_b)`
- El valor del slider se guarda como `final_pts_a` en `session_state`.

#### Step 1 — Datos de entrega

- Formulario con Email, Nombre y Dirección.
- Informativo; no persiste en esta versión.

#### Step 2 — Pago

Calcula el excedente a pagar en COP:

```python
excedente_pts = total_a - final_pts_a
monto_cop     = excedente_pts * 10   # 1 pt = $10 COP
```


- Si `excedente > 0`: muestra pasarela simulada con datos prediligenciados:
  - Tarjeta: `4532 0123 4567 8901` · Vencimiento: `12/28` · CVV: `•••`
- Si `excedente = 0`: se cubre 100% con puntos, no se muestra pasarela.

#### Step 3 — Confirmación

```python
puntos_descontados = total_b + final_pts_a
usuario['puntos'] -= puntos_descontados
save_users_to_db()   # Persiste el nuevo saldo
clear_cart()         # Vacía el carrito
```

Muestra animación de éxito y la opción de volver al catálogo.

---

### Tabla de validaciones

| Condición | Resultado |
|-----------|-----------|
| `puntos >= mínimo requerido` | ✅ Puede continuar al checkout |
| `puntos < mínimo requerido` | ❌ Muestra déficit en puntos |
| Solo Bonos (Tipo B) | Sin slider — pago 100% en puntos |
| Solo Tecnología (Tipo A) | Slider determina el split pts / COP |
| Carrito vacío | Botón de checkout oculto |

---

## 🛠️ Panel de administración

Accesible con cupón `admin`:

- Estadísticas globales: usuarios activos y puntos totales del sistema.
- Listado completo de usuarios con saldos.
- Control del **porcentaje mínimo de redención en Tecnología** (deslizador 0–100%).

---

## 🗂️ Estructura del proyecto

```
prueba_juju/
├── app.py              # UI + lógica completa
├── init_db.py          # Script de inicialización
├── database.xlsx       # BD Excel (hojas: Users, Products, Config)
├── requirements.txt
└── inspiración/
    ├── Logo empresa Alpha.png
    └── diagrama implementación carrito.png
```

---

## 📦 Dependencias

| Paquete | Uso |
|---------|-----|
| `streamlit` | Framework web |
| `pandas` | Lectura/escritura Excel |
| `openpyxl` | Motor `.xlsx` |
| `Pillow` | Carga de imágenes |

---

> ⚠️ Aplicación de uso personal. Los datos de tarjeta son **100% simulados**. No se procesa ningún pago real.
