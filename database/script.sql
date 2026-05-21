CREATE TABLE Conversaciones (
    id         INT IDENTITY(1,1) PRIMARY KEY,
    usuario    VARCHAR(100),
    mensaje    NVARCHAR(MAX),
    intencion  VARCHAR(60),
    confianza  DECIMAL(5,4),
    respuesta  NVARCHAR(MAX),
    fecha_hora DATETIME2 DEFAULT GETDATE()
);

CREATE TABLE Reservas (
    id             INT IDENTITY(1,1) PRIMARY KEY,
    nombre_cliente VARCHAR(100),
    fecha          VARCHAR(50),
    hora           VARCHAR(20),
    num_personas   INT,
    estado         VARCHAR(20) DEFAULT 'Confirmada',
    fecha_creacion DATETIME2 DEFAULT GETDATE()
);

CREATE TABLE Pedidos (
    id             INT IDENTITY(1,1) PRIMARY KEY,
    nombre_cliente VARCHAR(100),
    detalle        NVARCHAR(MAX),
    estado         VARCHAR(30) DEFAULT 'En preparación',
    fecha_hora     DATETIME2 DEFAULT GETDATE()
);

CREATE TABLE Platos (
    id         INT IDENTITY(1,1) PRIMARY KEY,
    categoria  VARCHAR(50),
    nombre     VARCHAR(100),
    precio     DECIMAL(6,2),
    disponible BIT DEFAULT 1
);

INSERT INTO Platos (categoria, nombre, precio) VALUES
('Entradas', 'Causa limeña rellena', 18.00),
('Entradas', 'Tequeños de queso',    16.00),
('Fondos',   'Ceviche clásico',      35.00),
('Fondos',   'Lomo saltado',         42.00),
('Fondos',   'Ají de gallina',       38.00),
('Postres',  'Suspiro limeño',       14.00),
('Postres',  'Arroz con leche',      12.00),
('Bebidas',  'Chicha morada',        10.00),
('Bebidas',  'Inca Kola / Coca-Cola',8.00);
