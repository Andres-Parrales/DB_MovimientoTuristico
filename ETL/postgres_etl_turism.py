# -*- coding: utf-8 -*-
import random
import pandas as pd
from sqlalchemy import create_engine
from faker import Faker
from tqdm import tqdm
import time

# ==========================================
# 1. CONFIGURACIÓN Y CONEXIÓN POSTGRESQL
# ==========================================

USER = "postgres"
PASSWORD = "YOU_PASSWORD"
HOST = "localhost"
PORT = "5432"
DB = "YOU_DATABASE_NAME"

try:
    engine = create_engine(
        f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    )

    pd.read_sql("SELECT 1", engine)
    print(f"✔ Conexión exitosa a PostgreSQL (Base de datos: {DB})\n")

except Exception as e:
    print(f"❌ Error al conectar a la base de datos: {e}")

    engine = create_engine(
        f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    )

# Faker en español
fake = Faker("es_ES")

# ==========================================
# 2. FUNCIONES ETL (NO CAMBIAN LÓGICA)
# ==========================================

def cargar_paises():
    paises = [
        ("Colombia", "COL"), ("Mexico", "MEX"), ("Peru", "PER"),
        ("Argentina", "ARG"), ("Chile", "CHL"), ("Brasil", "BRA")
    ]
    df = pd.DataFrame(paises, columns=["nombre_pais", "codigo_iso"])
    df.to_sql("paises", engine, if_exists="append", index=False)

def cargar_categorias():
    categorias = [
        ("Aventura", "Tours extremos y naturaleza"),
        ("Cultural", "Experiencias históricas"),
        ("Playa", "Destinos costeros"),
        ("Gastronomía", "Experiencias culinarias"),
        ("Ecoturismo", "Turismo sostenible")
    ]
    df = pd.DataFrame(categorias, columns=["nombre_categoria", "descripcion"])
    df.to_sql("categorias_tour", engine, if_exists="append", index=False)

def cargar_metodos_pago():
    metodos = [
        ("Tarjeta Crédito",), ("Tarjeta Débito",),
        ("Transferencia",), ("PSE",), ("Efectivo",)
    ]
    df = pd.DataFrame(metodos, columns=["nombre_metodo"])
    df.to_sql("metodos_pago", engine, if_exists="append", index=False)

def cargar_clientes():
    clientes = []
    for _ in range(5000):
        clientes.append([
            fake.first_name(),
            fake.last_name(),
            fake.unique.email(),
            fake.phone_number()[:30],
            fake.date_of_birth(minimum_age=18, maximum_age=65),
            random.choice(["M", "F", "Otro"]),
            fake.city(),
            fake.date_between("-3y", "today")
        ])

    df = pd.DataFrame(clientes, columns=[
        "nombre", "apellido", "email", "telefono",
        "fecha_nacimiento", "genero", "ciudad", "fecha_registro"
    ])

    df.to_sql("clientes", engine, if_exists="append", index=False)

def cargar_empleados():
    cargos = ["Asesor", "Supervisor", "Gerente", "Coordinador"]
    empleados = []

    for _ in range(100):
        empleados.append([
            fake.first_name(),
            fake.last_name(),
            random.choice(cargos),
            fake.date_between("-5y", "-1y"),
            round(random.uniform(1800000, 7000000), 2),
            True
        ])

    df = pd.DataFrame(empleados, columns=[
        "nombre", "apellido", "cargo",
        "fecha_contratacion", "salario", "activo"
    ])

    df.to_sql("empleados", engine, if_exists="append", index=False)

def cargar_destinos():
    df_paises = pd.read_sql("SELECT * FROM paises", engine)
    destinos = []

    for _ in range(200):
        pais = df_paises.sample(1).iloc[0]
        destinos.append([
            fake.city()[:150],
            int(pais["id_pais"]),
            fake.city()[:100],
            random.choice(["Playa", "Montaña", "Ciudad", "Selva"])
        ])

    df = pd.DataFrame(destinos, columns=[
        "nombre_destino", "id_pais", "ciudad", "categoria_destino"
    ])

    df.to_sql("destinos", engine, if_exists="append", index=False)

def cargar_tours():
    df_destinos = pd.read_sql("SELECT * FROM destinos", engine)
    df_categorias = pd.read_sql("SELECT * FROM categorias_tour", engine)

    tours = []

    for _ in range(500):
        destino = df_destinos.sample(1).iloc[0]
        categoria = df_categorias.sample(1).iloc[0]

        tours.append([
            f"Tour {fake.word()} {fake.random_number(3)}"[:150],
            int(destino["id_destino"]),
            int(categoria["id_categoria"]),
            round(random.uniform(500000, 5000000), 2),
            random.randint(2, 15),
            random.randint(5, 40),
            True
        ])

    df = pd.DataFrame(tours, columns=[
        "nombre_tour", "id_destino", "id_categoria",
        "precio_base", "duracion_dias",
        "capacidad_maxima", "activo"
    ])

    df.to_sql("tours", engine, if_exists="append", index=False)

def cargar_reservas():
    df_clientes = pd.read_sql("SELECT * FROM clientes", engine)
    df_empleados = pd.read_sql("SELECT * FROM empleados", engine)
    df_tours = pd.read_sql("SELECT * FROM tours", engine)

    reservas = []

    for _ in range(50000):
        cliente = df_clientes.sample(1).iloc[0]
        empleado = df_empleados.sample(1).iloc[0]
        tour = df_tours.sample(1).iloc[0]

        personas = random.randint(1, 6)
        subtotal = float(tour["precio_base"]) * personas
        descuento = round(subtotal * 0.1, 2) if random.random() < 0.3 else 0
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

    df = pd.DataFrame(reservas, columns=[
        "id_cliente", "id_tour", "id_empleado",
        "fecha_reserva", "cantidad_personas", "estado",
        "subtotal", "descuento", "total"
    ])

    df.to_sql("reservas", engine, if_exists="append", index=False)

def cargar_pagos():
    df_reservas = pd.read_sql("SELECT * FROM reservas", engine)
    df_metodos = pd.read_sql("SELECT * FROM metodos_pago", engine)

    pagos = []

    for _, r in df_reservas.iterrows():
        metodo = df_metodos.sample(1).iloc[0]

        pagos.append([
            int(r["id_reserva"]),
            int(metodo["id_metodo_pago"]),
            fake.date_between("-2y", "today"),
            float(r["total"]),
            fake.uuid4()[:100]
        ])

    df = pd.DataFrame(pagos, columns=[
        "id_reserva", "id_metodo_pago",
        "fecha_pago", "monto", "referencia_pago"
    ])

    df.to_sql("pagos", engine, if_exists="append", index=False)

def cargar_evaluaciones():
    df_reservas = pd.read_sql("SELECT * FROM reservas", engine)

    evaluaciones = []

    for _, r in df_reservas.iterrows():
        if random.random() < 0.7:
            evaluaciones.append([
                int(r["id_reserva"]),
                random.randint(1, 5),
                fake.sentence(),
                fake.date_between("-2y", "today")
            ])

    df = pd.DataFrame(evaluaciones, columns=[
        "id_reserva", "puntuacion",
        "comentario", "fecha_evaluacion"
    ])

    df.to_sql("evaluaciones", engine, if_exists="append", index=False)

# ==========================================
# 3. PIPELINE ETL
# ==========================================

pasos_etl = [
    {"nombre": "Países", "funcion": cargar_paises},
    {"nombre": "Categorías", "funcion": cargar_categorias},
    {"nombre": "Métodos Pago", "funcion": cargar_metodos_pago},
    {"nombre": "Clientes", "funcion": cargar_clientes},
    {"nombre": "Empleados", "funcion": cargar_empleados},
    {"nombre": "Destinos", "funcion": cargar_destinos},
    {"nombre": "Tours", "funcion": cargar_tours},
    {"nombre": "Reservas", "funcion": cargar_reservas},
    {"nombre": "Pagos", "funcion": cargar_pagos},
    {"nombre": "Evaluaciones", "funcion": cargar_evaluaciones},
]

print("Iniciando ETL en PostgreSQL...\n")

with tqdm(total=len(pasos_etl)) as pbar:
    for paso in pasos_etl:
        try:
            paso["funcion"]()
            tqdm.write(f"✔ {paso['nombre']} OK")
        except Exception as e:
            tqdm.write(f"❌ Error en {paso['nombre']}: {e}")
            break
        pbar.update(1)

print("\n✔ ETL finalizado en PostgreSQL")
