import sqlite3
from datetime import datetime

import gi

import Metodos
from Conexion.conexionDB import ConexionBD
from Metodos.metodosBotones import cargar_datos

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import webbrowser


class FiestraPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Peluquería")
        self.set_border_width(10)


        caja_horizontal = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.add(caja_horizontal)

        cuadro1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        cuadro1.set_size_request(300, 300)
        color1 = Gdk.RGBA()
        color1.parse('#FFFFFF')
        cuadro1.override_background_color(Gtk.StateFlags.NORMAL, color1)
        imagen1 = Gtk.Image.new_from_file("/home/dam/PycharmProjects/Peluqueria/Imagenes/Logo.png")

        texto = "<a href='http://www.ejemplo.com'>Nuestra página</a>"
        lblEnlace = Gtk.Label(label=texto)
        lblEnlace.set_use_markup(True)
        lblEnlace.connect("activate-link", self.enlace_activado)

        cuadro1.pack_start(imagen1, True, True, 0)
        cuadro1.pack_start(lblEnlace, False, False, 0)

        cuadro2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        cuadro2.set_size_request(400, 400)
        color2 = Gdk.RGBA()
        color2.parse('#4682B4')
        cuadro2.override_background_color(Gtk.StateFlags.NORMAL, color2)

        caja_nombre = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        caja_nombre.set_halign(Gtk.Align.CENTER)

        lblNombre = Gtk.Label(label="Nombre de usuario")
        lblNombre.set_halign(Gtk.Align.CENTER)

        self.txtNombre = Gtk.Entry()
        self.txtNombre.set_width_chars(20)
        self.txtNombre.set_halign(Gtk.Align.CENTER)

        caja_nombre.pack_start(lblNombre, False, False, 0)
        caja_nombre.pack_start(self.txtNombre, False, False, 0)

        caja_contraseña = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        caja_contraseña.set_halign(Gtk.Align.CENTER)

        lblContraseña = Gtk.Label(label="Contraseña del usuario")
        lblContraseña.set_halign(Gtk.Align.CENTER)
        self.txtContraseña = Gtk.Entry()
        self.txtContraseña.set_visibility(False)
        self.txtContraseña.set_width_chars(20)
        self.txtContraseña.set_halign(Gtk.Align.CENTER)

        caja_contraseña.pack_start(lblContraseña, False, False, 0)
        caja_contraseña.pack_start(self.txtContraseña, False, False, 0)

        caixaBtnAceptar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        self.btnAceptar = Gtk.Button(label="Aceptar")
        self.btnAceptar.connect("clicked", self.on_btnAceptar_clicked, self)
        caixaBtnAceptar.set_halign(Gtk.Align.CENTER)
        caixaBtnAceptar.pack_start(self.btnAceptar, False, False, 2)

        texto = "<a href='abrir_ventana'>Registrarse</a>"
        lblEnlace2 = Gtk.Label(label=texto)
        lblEnlace2.set_use_markup(True)
        lblEnlace2.connect("activate-link", self.registro)

        cuadro2.pack_start(caja_nombre, False, False, 10)
        cuadro2.pack_start(caja_contraseña, False, False, 10)
        cuadro2.pack_start(caixaBtnAceptar, False, False, 10)
        cuadro2.pack_start(lblEnlace2, False, False, 10)

        grid = Gtk.Grid()
        grid.add(cuadro2)

        caja_horizontal.pack_start(cuadro1, True, True, 0)
        caja_horizontal.pack_start(grid, True, True, 0)


        cuadro2.pack_start(caja_nombre, False, False, 10)
        cuadro2.pack_start(caja_contraseña, False, False, 10)

        grid = Gtk.Grid()
        grid.add(cuadro2)

        caja_horizontal.pack_start(cuadro1, True, True, 0)
        caja_horizontal.pack_start(grid, True, True, 0)

    def on_btnAceptar_clicked(self, widget, ventana_a_ocultar):
        # Crear conexión y cursor a la base de datos
        conBD = ConexionBD("Peluqueria.sqlite")
        conBD.conectaBD()
        conBD.creaCursor()

        # Crear nueva ventana
        nueva_ventana = Gtk.Window(title="Base de datos")
        nueva_ventana.set_default_size(700, 400)

        # Caja principal vertical
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        nueva_ventana.add(vbox)

        # --- Encabezado personalizado encima del TreeView ---
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        # Imagen de encabezado (ruta válida)
        imagen1 = Gtk.Image.new_from_file("/home/dam/PycharmProjects/Peluqueria/Imagenes/Logo.png")
        header_box.pack_start(imagen1, False, False, 5)

        # Añadimos el header personalizado al vbox
        vbox.pack_start(header_box, False, False, 0)

        # Crear modelo ListStore
        liststore = Gtk.ListStore(int, str, str, int, str, int, int)

        # Ejecutar consulta y llenar el liststore
        conBD.cursor.execute(
            "SELECT Id, Nombre, Apellidos, HoraCita, Servicios, Total_Gastado, id_Peluquera FROM Clientes")
        for fila in conBD.cursor.fetchall():
            liststore.append(fila)

        # Crear TreeView con el modelo
        treeview = Gtk.TreeView(model=liststore)

        # Crear columnas de texto
        titulos = ["ID", "Nombre", "Apellidos", "HoraCita", "Servicios", "Total_Gastado", "id_Peluquera"]
        for i, columna_titulo in enumerate(titulos):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(columna_titulo, renderer, text=i)
            treeview.append_column(column)

        # Scroll para el treeview
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)
        scrolled_window.add(treeview)

        # Caja horizontal para el TreeView y el botón
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        # Añadir el scrolled window (con TreeView) a la izquierda
        hbox.pack_start(scrolled_window, True, True, 0)

        botones_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        # Crear botón a la derecha
        botonAgregar = Gtk.Button(label="Agregar")
        botonBorrar = Gtk.Button(label="Borrar")
        botonEditar = Gtk.Button(label="Editar")
        botones_box.pack_start(botonAgregar, False, False, 0)
        botones_box.pack_start(botonBorrar, False, False, 0)
        botones_box.pack_start(botonEditar, False, False, 0)

        #botonAgregar.connect("clicked", on_btnAgregar_clicked,self)
        cargar_datos(self)

        search_entry = Gtk.SearchEntry()
        botones_box.pack_start(search_entry, False, False, 10)

        hbox.pack_start(botones_box, False, False, 10)


        vbox.pack_start(hbox, True, True, 0)

        lblInsertor = Gtk.Label("Introduzca el cambio")
        insertor = Gtk.Entry()
        vbox.pack_start(lblInsertor, True, True, 0)
        vbox.pack_start(insertor, True, True, 0)


        # Conectar señal para cerrar ventana
        nueva_ventana.connect("destroy", Gtk.main_quit)

        # Mostrar ventana
        nueva_ventana.show_all()

        # Ocultar ventana original
        ventana_a_ocultar.hide()

    def enlace_activado(self, widget, uri):
        print(f"Enlace activado: {uri}")
        webbrowser.open(uri)

    def registro(self, widget, uri):
        if uri == "abrir_ventana":
            nueva_ventana = Gtk.Window(title="Registro")
            nueva_ventana.set_default_size(400, 400)



            cuadro_nueva = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
            color = Gdk.RGBA()
            color.parse('#4682B4')
            cuadro_nueva.override_background_color(Gtk.StateFlags.NORMAL, color)
            nueva_ventana.add(cuadro_nueva)

            cuadro1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            cuadro1.set_size_request(300, 300)
            color1 = Gdk.RGBA()
            color1.parse('#FFFFFF')
            cuadro1.override_background_color(Gtk.StateFlags.NORMAL, color1)
            imagen1 = Gtk.Image.new_from_file("/home/dam/PycharmProjects/Peluqueria/Imagenes/Logo.png")

            texto = "<a href='http://www.ejemplo.com'>Nuestra página</a>"
            lblEnlace = Gtk.Label(label=texto)
            lblEnlace.set_use_markup(True)
            lblEnlace.connect("activate-link", self.enlace_activado)

            cuadro1.pack_start(imagen1, True, True, 0)
            cuadro1.pack_start(lblEnlace, False, False, 0)

            # Campo nombre
            caja_nombre = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            caja_nombre.set_halign(Gtk.Align.CENTER)
            lblNombre = Gtk.Label(label="Nombre de usuario")
            lblNombre.set_halign(Gtk.Align.CENTER)
            txtNombre = Gtk.Entry()
            txtNombre.set_width_chars(20)
            txtNombre.set_halign(Gtk.Align.CENTER)
            caja_nombre.pack_start(lblNombre, False, False, 0)
            caja_nombre.pack_start(txtNombre, False, False, 0)

            # Campo contraseña
            lblContraseña = Gtk.Label(label="Contraseña del usuario")
            lblContraseña.set_halign(Gtk.Align.CENTER)
            txtContraseña = Gtk.Entry()
            txtContraseña.set_visibility(False)
            txtContraseña.set_width_chars(20)
            txtContraseña.set_halign(Gtk.Align.CENTER)
            caja_nombre.pack_start(lblContraseña, False, False, 0)
            caja_nombre.pack_start(txtContraseña, False, False, 0)


            lblEmail = Gtk.Label(label="Email")
            lblEmail.set_halign(Gtk.Align.CENTER)
            txtEmail = Gtk.Entry()
            txtEmail.set_width_chars(20)
            txtEmail.set_halign(Gtk.Align.CENTER)
            caja_nombre.pack_start(lblEmail, False, False, 0)
            caja_nombre.pack_start(txtEmail, False, False, 0)

            lblTelefono = Gtk.Label(label="Telefono")
            lblTelefono.set_halign(Gtk.Align.CENTER)
            txtTelefono = Gtk.Entry()
            txtTelefono.set_width_chars(20)
            txtTelefono.set_halign(Gtk.Align.CENTER)
            caja_nombre.pack_start(lblTelefono, False, False, 0)
            caja_nombre.pack_start(txtTelefono, False, False, 0)

            btnAceptar = Gtk.Button(label="Aceptar")
            btnAceptar.connect("clicked", self.on_btnAceptar_clicked, nueva_ventana)

            cuadro_nueva.pack_start(cuadro1, False, False, 10)
            cuadro_nueva.pack_start(caja_nombre, False, False, 10)


            # Mostrar ventana y cerrar la principal
            nueva_ventana.connect("destroy", Gtk.main_quit)
            nueva_ventana.show_all()
            self.hide()

            return True
        return False


if __name__ == "__main__":
    ventana = FiestraPrincipal()
    ventana.connect("destroy", Gtk.main_quit)
    ventana.show_all()
    Gtk.main()
