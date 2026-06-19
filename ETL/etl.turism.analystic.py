# -*- coding: utf-8 -*-
import random
import pandas as pd
from sqlalchemy import create_engine
from faker import Faker
from tqdm import tqdm
import time

# ==========================================
# 1. CONFIGURACIÓN Y CONEXIÓN BASE
# ==========================================

USER = "root"
PASSWORD = "Cualquiera1"
HOST = "localhost"
DB = "Base_datosTuristica"

try:
    engine = create_engine(
        f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB}"
    )

    pd.read_sql("SELECT 1", engine)
    print(f"✔ Conexión exitosa a MySQL (Base de datos: {DB})\n")

except Exception as e:
    print(f"❌ Error al conectar a la base de datos: {e}")
    print("Asegúrate de que MySQL esté activo, las credenciales sean correctas y la base de datos exista.\n")

    engine = create_engine(
        f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB}"
    )

# Inicializar Faker en español
fake = Faker("es_ES")

# ==========================================
# 2. DEFINICIÓN DE PASOS DEL PROCESO ETL
# ==========================================

def cargar_paises():
    paises = [
        ("Colombia", "COL"), ("Mexico", "MEX"), ("Peru", "PER"),
        ("Argentina", "ARG"), ("Chile", "CHL"), ("Brasil", "BRA")
    ]
    df_paises = pd.DataFrame(paises, columns=["nombre_pais", "codigo_iso"])
    df_paises.to_sql("paises", engine, if_exists="append", index=False)

def cargar_categorias():
    categorias = [
        ("Aventura", "Tours extremos y naturaleza"),
        ("Cultural", "Experiencias históricas"),
        ("Playa", "Destinos costeros"),
        ("Gastronomía", "Experiencias culinarias"),
        ("Ecoturismo", "Turismo sostenible")
    ]
    df_categorias = pd.DataFrame(categorias, columns=["nombre_categoria", "descripcion"])
    df_categorias.to_sql("categorias_tour", engine, if_exists="append", index=False)

def cargar_metodos_pago():
    metodos = [
        ("Tarjeta Crédito",), ("Tarjeta Débito",),
        ("Transferencia",), ("PSE",), ("Efectivo",)
    ]
    df_metodos = pd.DataFrame(metodos, columns=["nombre_metodo"])
    df_metodos.to_sql("metodos_pago", engine, if_exists="append", index=False)

def cargar_clientes():
    clientes = []
    for _ in range(5000):
        clientes.append([
            fake.first_name(),
            fake.last_name(),
            fake.unique.email(),  # Asegura unicidad para la restricción UNIQUE del SQL
            fake.phone_number()[:30],  # Recorte preventivo para el VARCHAR(30)
            fake.date_of_birth(minimum_age=18, maximum_age=65),
            random.choice(["M", "F", "Otro"]),
            fake.city(),
            fake.date_between("-3y", "today")
        ])
    df_clientes = pd.DataFrame(clientes, columns=[
        "nombre", "apellido", "email", "telefono",
        "fecha_nacimiento", "genero", "ciudad", "fecha_registro"
    ])
    df_clientes.to_sql("clientes", engine, if_exists="append", index=False)

def cargar_empleados():
    empleados = []
    cargos = ["Asesor", "Supervisor", "Gerente", "Coordinador"]
    for _ in range(100):
        empleados.append([
            fake.first_name(),
            fake.last_name(),
            random.choice(cargos),
            fake.date_between("-5y", "-1y"),
            round(random.uniform(1800000, 7000000), 2),  # Formato DECIMAL(12,2)
            1
        ])
    df_empleados = pd.DataFrame(empleados, columns=[
        "nombre", "apellido", "cargo", "fecha_contratacion", "salario", "activo"
    ])
    df_empleados.to_sql("empleados", engine, if_exists="append", index=False)

def cargar_destinos():
    df_paises_db = pd.read_sql("SELECT * FROM paises", engine)
    destinos = []
    for _ in range(200):
        pais = df_paises_db.sample(1).iloc[0]
        destinos.append([
            fake.city()[:150],
            int(pais["id_pais"]),
            fake.city()[:100],
            random.choice(["Playa", "Montaña", "Ciudad", "Selva"])
        ])
    df_destinos = pd.DataFrame(destinos, columns=[
        "nombre_destino", "id_pais", "ciudad", "categoria_destino"
    ])
    df_destinos.to_sql("destinos", engine, if_exists="append", index=False)

def cargar_tours():
    df_destinos_db = pd.read_sql("SELECT * FROM destinos", engine)
    df_categorias_db = pd.read_sql("SELECT * FROM categorias_tour", engine)
    tours = []
    for _ in range(500):
        destino = df_destinos_db.sample(1).iloc[0]
        categoria = df_categorias_db.sample(1).iloc[0]
        tours.append([
            f"Tour {fake.word()} {fake.random_number(3)}"[:150],
            int(destino["id_destino"]),
            int(categoria["id_categoria"]),
            round(random.uniform(500000, 5000000), 2),
            random.randint(2, 15),
            random.randint(5, 40),
            1
        ])
    df_tours = pd.DataFrame(tours, columns=[
        "nombre_tour", "id_destino", "id_categoria",
        "precio_base", "duracion_dias", "capacidad_maxima", "activo"
    ])
    df_tours.to_sql("tours", engine, if_exists="append", index=False)

def cargar_reservas():
    df_clientes_db = pd.read_sql("SELECT * FROM clientes", engine)
    df_empleados_db = pd.read_sql("SELECT * FROM empleados", engine)
    df_tours_db = pd.read_sql("SELECT * FROM tours", engine)
    reservas = []
    for _ in range(50000):
        cliente = df_clientes_db.sample(1).iloc[0]
        empleado = df_empleados_db.sample(1).iloc[0]
        tour = df_tours_db.sample(1).iloc[0]

        personas = random.randint(1, 6)
        subtotal = float(tour["precio_base"]) * personas
        descuento = random.choice([0.0, 0.0, 0.0, round(subtotal * 0.1, 2)])
        total = subtotal - descuento

        reservas.append([
            int(cliente["id_cliente"]),
            int(tour["id_tour"]),
            int(empleado["id_empleado"]),
            fake.date_between("-2y", "today"),
            personas,
            random.choice(["Pendiente", "Confirmada", "Cancelada"]),
            round(subtotal, 2),
            round(descuento, 2),
            round(total, 2)
        ])
    df_reservas = pd.DataFrame(reservas, columns=[
        "id_cliente", "id_tour", "id_empleado",
        "fecha_reserva", "cantidad_personas", "estado",
        "subtotal", "descuento", "total"
    ])
    df_reservas.to_sql("reservas", engine, if_exists="append", index=False)

def cargar_pagos():
    df_reservas_db = pd.read_sql("SELECT * FROM reservas", engine)
    df_metodos_db = pd.read_sql("SELECT * FROM metodos_pago", engine)
    pagos = []
    for _, r in df_reservas_db.iterrows():
        metodo = df_metodos_db.sample(1).iloc[0]
        pagos.append([
            int(r["id_reserva"]),
            int(metodo["id_metodo_pago"]),
            fake.date_between("-2y", "today"),
            round(float(r["total"]), 2),
            fake.uuid4()[:100]
        ])
    df_pagos = pd.DataFrame(pagos, columns=[
        "id_reserva", "id_metodo_pago", "fecha_pago", "monto", "referencia_pago"
    ])
    df_pagos.to_sql("pagos", engine, if_exists="append", index=False)

def cargar_evaluaciones():
    df_reservas_db = pd.read_sql("SELECT * FROM reservas", engine)
    evaluaciones = []
    for _, r in df_reservas_db.iterrows():
        if random.random() < 0.7:
            evaluaciones.append([
                int(r["id_reserva"]),
                random.randint(1, 5),
                fake.sentence(),
                fake.date_between("-2y", "today")
            ])
    df_eval = pd.DataFrame(evaluaciones, columns=[
        "id_reserva", "puntuacion", "comentario", "fecha_evaluacion"
    ])
    df_eval.to_sql("evaluaciones", engine, if_exists="append", index=False)

# ==========================================
# 3. EJECUCIÓN ORDENADA CON BARRA DE PROGRESO
# ==========================================

pasos_etl = [
    {"nombre": "1. Países", "funcion": cargar_paises},
    {"nombre": "2. Categorías de Tour", "funcion": cargar_categorias},
    {"nombre": "3. Métodos de Pago", "funcion": cargar_metodos_pago},
    {"nombre": "4. Clientes", "funcion": cargar_clientes},
    {"nombre": "5. Empleados", "funcion": cargar_empleados},
    {"nombre": "6. Destinos", "funcion": cargar_destinos},
    {"nombre": "7. Tours", "funcion": cargar_tours},
    {"nombre": "8. Reservas (Fact)", "funcion": cargar_reservas},
    {"nombre": "9. Pagos", "funcion": cargar_pagos},
    {"nombre": "10. Evaluaciones", "funcion": cargar_evaluaciones},
]

print("Iniciando la carga ordenada del pipeline ETL...\n")

# Estructura limpia usando un manejador de contexto tqdm
with tqdm(total=len(pasos_etl), desc="Progreso ETL Total", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]") as pbar:
    for paso in pasos_etl:
        pbar.set_postfix_str(f"Procesando {paso['nombre']}...")
        start_time = time.time()
        
        try:
            paso["funcion"]()
            end_time = time.time()
            tqdm.write(f"✔ {paso['nombre']} completado exitosamente en {end_time - start_time:.2f}s.")
        except Exception as e:
            tqdm.write(f"❌ Error crítico en el paso [{paso['nombre']}]: {e}")
            break
            
        pbar.update(1)

print("\n¡Pipeline ETL finalizado exitosamente!")