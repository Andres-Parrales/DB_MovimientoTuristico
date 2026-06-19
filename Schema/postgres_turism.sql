-- =========================================
-- TABLAS DIMENSIONALES
-- =========================================

-- PAÍSES
CREATE TABLE paises (
    id_pais INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_pais VARCHAR(100) NOT NULL UNIQUE,
    codigo_iso CHAR(3) NOT NULL UNIQUE
);

-- CATEGORÍAS DE TOUR
CREATE TABLE categorias_tour (
    id_categoria INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_categoria VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT
);

-- MÉTODOS DE PAGO
CREATE TABLE metodos_pago (
    id_metodo_pago INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_metodo VARCHAR(50) NOT NULL UNIQUE
);

-- CLIENTES
CREATE TABLE clientes (
    id_cliente INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    telefono VARCHAR(30),
    fecha_nacimiento DATE,
    genero VARCHAR(20),
    ciudad VARCHAR(100),
    fecha_registro DATE NOT NULL
);

-- EMPLEADOS
CREATE TABLE empleados (
    id_empleado INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cargo VARCHAR(100),
    fecha_contratacion DATE,
    salario DECIMAL(12,2),
    activo BOOLEAN DEFAULT TRUE
);

-- =========================================
-- GEOGRAFÍA / PRODUCTO
-- =========================================

-- DESTINOS
CREATE TABLE destinos (
    id_destino INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_destino VARCHAR(150) NOT NULL,
    id_pais INT NOT NULL,
    ciudad VARCHAR(100),
    categoria_destino VARCHAR(50),

    CONSTRAINT fk_destino_pais
        FOREIGN KEY (id_pais)
        REFERENCES paises(id_pais)
        ON DELETE RESTRICT
);

-- TOURS
CREATE TABLE tours (
    id_tour INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_tour VARCHAR(150) NOT NULL,
    id_destino INT NOT NULL,
    id_categoria INT NOT NULL,
    precio_base DECIMAL(12,2) NOT NULL,
    duracion_dias INT NOT NULL,
    capacidad_maxima INT NOT NULL,
    activo BOOLEAN DEFAULT TRUE,

    CONSTRAINT fk_tour_destino
        FOREIGN KEY (id_destino)
        REFERENCES destinos(id_destino)
        ON DELETE RESTRICT,

    CONSTRAINT fk_tour_categoria
        FOREIGN KEY (id_categoria)
        REFERENCES categorias_tour(id_categoria)
        ON DELETE RESTRICT
);

-- =========================================
-- HECHOS (FACT TABLES)
-- =========================================

-- RESERVAS
CREATE TABLE reservas (
    id_reserva INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_tour INT NOT NULL,
    id_empleado INT NOT NULL,

    fecha_reserva DATE NOT NULL,
    cantidad_personas INT NOT NULL,

    estado VARCHAR(50),

    subtotal DECIMAL(12,2),
    descuento DECIMAL(12,2),
    total DECIMAL(12,2),

    CONSTRAINT fk_reserva_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
        ON DELETE RESTRICT,

    CONSTRAINT fk_reserva_tour
        FOREIGN KEY (id_tour)
        REFERENCES tours(id_tour)
        ON DELETE RESTRICT,

    CONSTRAINT fk_reserva_empleado
        FOREIGN KEY (id_empleado)
        REFERENCES empleados(id_empleado)
        ON DELETE RESTRICT
);

-- PAGOS
CREATE TABLE pagos (
    id_pago INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_reserva INT NOT NULL,
    id_metodo_pago INT NOT NULL,

    fecha_pago DATE NOT NULL,
    monto DECIMAL(12,2) NOT NULL,
    referencia_pago VARCHAR(100),

    CONSTRAINT fk_pago_reserva
        FOREIGN KEY (id_reserva)
        REFERENCES reservas(id_reserva)
        ON DELETE CASCADE,

    CONSTRAINT fk_pago_metodo
        FOREIGN KEY (id_metodo_pago)
        REFERENCES metodos_pago(id_metodo_pago)
        ON DELETE RESTRICT
);

-- EVALUACIONES
CREATE TABLE evaluaciones (
    id_evaluacion INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_reserva INT NOT NULL,

    puntuacion INT NOT NULL,
    comentario TEXT,
    fecha_evaluacion DATE,

    CONSTRAINT fk_evaluacion_reserva
        FOREIGN KEY (id_reserva)
        REFERENCES reservas(id_reserva)
        ON DELETE CASCADE
);

-- =========================================
-- TABLA CALENDARIO
-- =========================================

CREATE TABLE calendario (
    id_fecha DATE PRIMARY KEY,
    anio INT,
    trimestre INT,
    mes INT,
    nombre_mes VARCHAR(20),
    semana INT,
    dia INT,
    nombre_dia VARCHAR(20)
);