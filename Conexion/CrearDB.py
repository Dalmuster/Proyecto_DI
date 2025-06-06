import sqlite3

conexion = sqlite3.connect("../UI/Peluqueria.sqlite")
cursor = conexion.cursor()

script_sql = """
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Clientes" (
    "Id"    INTEGER NOT NULL UNIQUE,
    "Nombre"    TEXT NOT NULL,
    "Apellidos" TEXT NOT NULL,
    "HoraCita"  INTEGER NOT NULL,
    "Servicios" TEXT,
    "Total_Gastado" INTEGER,
    "id_Peluquera"  INTEGER,
    PRIMARY KEY("Id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Usuarios" (
    "Id"    INTEGER NOT NULL,
    "Nombre"    TEXT NOT NULL UNIQUE,
    "Contraseña"    TEXT NOT NULL,
    "Correo"    INTEGER NOT NULL,
    PRIMARY KEY("Id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Peluqueras" (
    "Id"    INTEGER NOT NULL UNIQUE,
    "Nombre"    TEXT NOT NULL,
    "Apellidos" TEXT NOT NULL,
    "Servicios" TEXT,
    "NumeroServicios" INTEGER NOT NULL,
    "Sueldo"    INTEGER NOT NULL,
    PRIMARY KEY("Id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Administradores" (
    "Id"    INTEGER NOT NULL UNIQUE,
    "Nombre"    TEXT NOT NULL,
    "Apellidos" TEXT NOT NULL,
    "Correo"    TEXT NOT NULL,
    PRIMARY KEY("Id" AUTOINCREMENT)
);
COMMIT;
"""

cursor.executescript(script_sql)
conexion.commit()
conexion.close()
