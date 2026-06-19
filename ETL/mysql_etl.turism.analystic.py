
import random
import pandas as pd
from sqlalchemy import create_engine
from faker import Faker
from tqdm import tqdm
import time

# ==========================================
# 1. CONEXIÓN MYSQL
# ==========================================

USER = "root"
PASSWORD = "YOU_DB_PASSWORD"
HOST = "localhost"
DB = "Base_datosTuristica"

engine = create_engine(
    f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB}?charset=utf8mb4"
)

try:
    pd.read_sql("SELECT 1", engine)
    print("✔ Conexión exitosa a MySQL\n")
except Exception as e:
    print(f"❌ Error conexión: {e}")

fake = Faker("es_ES")

# ==========================================
# 2. DATA GEOGRÁFICA REAL (CLAVE)
# ==========================================

PAISES = {
    "Colombia": {
        "codigo": "COL",
        "ciudades": [
            "Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena",
            "Bucaramanga", "Pereira", "Santa Marta", "Manizales",
            "Villavicencio", "Cúcuta", "Pasto"
        ]
    },
    "Mexico": {
        "codigo": "MEX",
        "ciudades": [
            "Ciudad de México", "Guadalajara", "Monterrey",
            "Cancún", "Tulum", "Puebla", "Oaxaca", "Mérida"
        ]
    },
    "Peru": {
        "codigo": "PER",
        "ciudades": [
            "Lima", "Cusco", "Arequipa", "Trujillo", "Iquitos",
            "Puno", "Chiclayo"
        ]
    },
    "Argentina": {
        "codigo": "ARG",
        "ciudades": [
            "Buenos Aires", "Córdoba", "Rosario", "Mendoza",
            "Bariloche", "Salta"
        ]
    },
    "Chile": {
        "codigo": "CHL",
        "ciudades": [
            "Santiago", "Valparaíso", "Viña del Mar",
            "La Serena", "Concepción", "Punta Arenas"
        ]
    },
    "Brasil": {
        "codigo": "BRA",
        "ciudades": [
            "São Paulo", "Rio de Janeiro", "Brasília",
            "Salvador", "Fortaleza", "Manaus"
        ]
    }
}

CATEGORIAS = [
    ("Aventura", "Tours extremos"),
    ("Cultural", "Experiencias históricas"),
    ("Playa", "Destinos costeros"),
    ("Gastronomía", "Experiencias culinarias"),
    ("Ecoturismo", "Turismo sostenible")
]

# ==========================================
# 3. CLIENTES (MEJOR DISTRIBUCIÓN)
# ==========================================

def cargar_clientes():
    ciudades = [c for p in PAISES.values() for c in p["ciudades"]]

    data = []
    for _ in range(10000):
        data.append([
            fake.first_name(),
            fake.last_name(),
            fake.unique.email(),
            fake.phone_number()[:30],
            fake.date_of_birth(minimum_age=18, maximum_age=65),
            random.choice(["M", "F", "Otro"]),
            random.choice(ciudades),
            fake.date_between("-3y", "today")
        ])

    df = pd.DataFrame(data, columns=[
        "nombre", "apellido", "email", "telefono",
        "fecha_nacimiento", "genero", "ciudad", "fecha_registro"
    ])

    df.to_sql("clientes", engine, if_exists="append", index=False)

# ==========================================
# 4. EMPLEADOS
# ==========================================

def cargar_empleados():
    cargos = ["Asesor", "Supervisor", "Gerente", "Coordinador"]

    data = []
    for _ in range(200):
        data.append([
            fake.first_name(),
            fake.last_name(),
            random.choice(cargos),
            fake.date_between("-5y", "-1y"),
            round(random.uniform(1800000, 9000000), 2),
            1
        ])

    df = pd.DataFrame(data, columns=[
        "nombre", "apellido", "cargo",
        "fecha_contratacion", "salario", "activo"
    ])

    df.to_sql("empleados", engine, if_exists="append", index=False)

# ==========================================
# 5. DESTINOS (MUCHO MÁS COHERENTES)
# ==========================================

def cargar_destinos():
    df_paises = pd.read_sql("SELECT * FROM paises", engine)

    data = []

    for _, pais in df_paises.iterrows():
        ciudades = PAISES[pais["nombre_pais"]]["ciudades"]

        for ciudad in ciudades:
            # 🔥 más volumen por ciudad
            for _ in range(8):
                data.append([
                    f"{ciudad} Experience",
                    int(pais["id_pais"]),
                    ciudad,
                    random.choice(["Playa", "Montaña", "Ciudad", "Selva", "Cultural"])
                ])

    df = pd.DataFrame(data, columns=[
        "nombre_destino", "id_pais", "ciudad", "categoria_destino"
    ])

    df.to_sql("destinos", engine, if_exists="append", index=False)

# ==========================================
# 6. TOURS (ESCALABLE)
# ==========================================

def cargar_tours():
    df_destinos = pd.read_sql("SELECT * FROM destinos", engine)
    df_cat = pd.read_sql("SELECT * FROM categorias_tour", engine)

    data = []

    for _ in range(6000):
        d = df_destinos.sample(1).iloc[0]
        c = df_cat.sample(1).iloc[0]

        data.append([
            f"Tour en {d['ciudad']} - {c['nombre_categoria']}",
            int(d["id_destino"]),
            int(c["id_categoria"]),
            round(random.uniform(200000, 7000000), 2),
            random.randint(1, 10),
            random.randint(5, 45),
            1
        ])

    df = pd.DataFrame(data, columns=[
        "nombre_tour", "id_destino", "id_categoria",
        "precio_base", "duracion_dias", "capacidad_maxima", "activo"
    ])

    df.to_sql("tours", engine, if_exists="append", index=False)

# ==========================================
# 7. RESERVAS (OPTIMIZADO)
# ==========================================

def cargar_reservas():
    clientes = pd.read_sql("SELECT id_cliente FROM clientes", engine)["id_cliente"].tolist()
    empleados = pd.read_sql("SELECT id_empleado FROM empleados", engine)["id_empleado"].tolist()
    tours = pd.read_sql("SELECT id_tour, precio_base FROM tours", engine)

    data = []

    for _ in range(60000):
        t = tours.sample(1).iloc[0]

        personas = random.randint(1, 6)
        subtotal = float(t["precio_base"]) * personas
        descuento = subtotal * 0.1 if random.random() < 0.25 else 0

        data.append([
            random.choice(clientes),
            int(t["id_tour"]),
            random.choice(empleados),
            fake.date_between("-2y", "today"),
            personas,
            random.choice(["Pendiente", "Confirmada", "Cancelada"]),
            subtotal,
            descuento,
            subtotal - descuento
        ])

    df = pd.DataFrame(data, columns=[
        "id_cliente", "id_tour", "id_empleado",
        "fecha_reserva", "cantidad_personas", "estado",
        "subtotal", "descuento", "total"
    ])

    df.to_sql("reservas", engine, if_exists="append", index=False)

# ==========================================
# 8. PAGOS
# ==========================================

def cargar_pagos():
    reservas = pd.read_sql("SELECT * FROM reservas", engine)
    metodos = pd.read_sql("SELECT * FROM metodos_pago", engine)

    data = []

    for _, r in reservas.iterrows():
        m = metodos.sample(1).iloc[0]

        data.append([
            int(r["id_reserva"]),
            int(m["id_metodo_pago"]),
            fake.date_between("-2y", "today"),
            float(r["total"]),
            fake.uuid4()[:80]
        ])

    df = pd.DataFrame(data, columns=[
        "id_reserva", "id_metodo_pago",
        "fecha_pago", "monto", "referencia_pago"
    ])

    df.to_sql("pagos", engine, if_exists="append", index=False)

# ==========================================
# 9. EVALUACIONES
# ==========================================

def cargar_evaluaciones():
    reservas = pd.read_sql("SELECT id_reserva FROM reservas", engine)

    data = []

    for _, r in reservas.iterrows():
        if random.random() < 0.65:
            data.append([
                int(r["id_reserva"]),
                random.randint(1, 5),
                fake.sentence(),
                fake.date_between("-2y", "today")
            ])

    df = pd.DataFrame(data, columns=[
        "id_reserva", "puntuacion",
        "comentario", "fecha_evaluacion"
    ])

    df.to_sql("evaluaciones", engine, if_exists="append", index=False)

# ==========================================
# 10. PIPELINE
# ==========================================

pasos = [
    ("Países", cargar_paises),
    ("Categorías", lambda: pd.DataFrame(CATEGORIAS, columns=["nombre_categoria","descripcion"]).to_sql("categorias_tour", engine, if_exists="append", index=False)),
    ("Métodos pago", lambda: pd.DataFrame([("Tarjeta",""),("PSE",)], columns=["nombre_metodo"]).to_sql("metodos_pago", engine, if_exists="append", index=False)),
    ("Clientes", cargar_clientes),
    ("Empleados", cargar_empleados),
    ("Destinos", cargar_destinos),
    ("Tours", cargar_tours),
    ("Reservas", cargar_reservas),
    ("Pagos", cargar_pagos),
    ("Evaluaciones", cargar_evaluaciones),
]

print("🚀 Iniciando ETL MySQL...\n")

with tqdm(total=len(pasos)) as pbar:
    for nombre, func in pasos:
        try:
            func()
            print(f"✔ {nombre} OK")
        except Exception as e:
            print(f"❌ Error en {nombre}: {e}")
            break
        pbar.update(1)

print("\n🎉 ETL FINALIZADO")