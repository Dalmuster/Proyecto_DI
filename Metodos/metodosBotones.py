from gi.overrides import Gtk, Gdk

from Conexion.conexionDB import ConexionBD


def on_btnAgregar_clicked(self, widget):
    # 1. Conectar a la base de datos
    conBD = ConexionBD("Peluqueria.sqlite")
    conBD.conectaBD()
    conBD.creaCursor()

    # 2. Definir el SQL de inserción
    insert_sql = """INSERT INTO Clientes 
                    (Nombre, Apellidos, HoraCita, Servicios, Total_Gastado, id_Peluquera) 
                    VALUES (?, ?, ?, ?, ?, ?)"""

    # 3. Obtener los datos (puedes recogerlos de entradas GTK, aquí son fijos como ejemplo)
    nombre = "Laura"
    apellidos = "Gómez"
    hora_cita = 1100
    servicios = "Corte y tinte"
    total_gastado = 35
    id_peluquera = 2

    # 4. Ejecutar la inserción
    conBD.engadeRexistro(insert_sql, nombre, apellidos, hora_cita, servicios, total_gastado, id_peluquera)
    self.cargar_datos()

def cargar_datos(self):
    self.liststore.clear()
    self.conBD.cursor.execute("SELECT Id, Nombre, Apellidos, HoraCita, Servicios, Total_Gastado, id_Peluquera FROM Clientes")
    for fila in self.conBD.cursor.fetchall():
        self.liststore.append(fila)

