import sqlite3
from datetime import datetime

import gi

import Metodos
from Conexion.conexionDB import ConexionBD
from fpdf import FPDF
import datetime

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import webbrowser
from fpdf import FPDF
import datetime

class FiestraPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Peluquería")
        self.set_border_width(10)
        self.set_resizable(False)

        self.ventana_login = self

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
        self.btnAceptar.connect("clicked", self.on_login_clicked)

        caixaBtnAceptar.set_halign(Gtk.Align.CENTER)
        caixaBtnAceptar.pack_start(self.btnAceptar, False, False, 2)

        texto = "<a href='abrir_ventana'>Registrarse</a>"
        lblEnlace2 = Gtk.Label(label=texto)
        lblEnlace2.set_use_markup(True)
        lblEnlace2.connect("activate-link", self.registro)

        contenedor_centrado = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        contenedor_centrado.set_halign(Gtk.Align.CENTER)
        contenedor_centrado.set_valign(Gtk.Align.CENTER)

        contenedor_centrado.pack_start(caja_nombre, False, False, 0)
        contenedor_centrado.pack_start(caja_contraseña, False, False, 0)
        contenedor_centrado.pack_start(caixaBtnAceptar, False, False, 0)
        contenedor_centrado.pack_start(lblEnlace2, False, False, 0)

        cuadro2.pack_start(contenedor_centrado, True, True, 0)

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

    def on_login_clicked(self, widget):
        nombre = self.txtNombre.get_text().strip()
        contraseña = self.txtContraseña.get_text().strip()

        if not nombre or not contraseña:
            self.mostrar_dialogo_error_Login("Por favor, complete todos los campos.")
            return

        try:
            conexion = sqlite3.connect("Peluqueria.sqlite")
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Usuarios WHERE nombre = ? AND contraseña = ?", (nombre, contraseña))
            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                print("Inicio de sesión exitoso.")
                self.on_btnAceptar_clicked(widget, self)  # Llama a tu función personalizada
            else:
                self.mostrar_dialogo_error_Login("Usuario o contraseña incorrectos.")

        except Exception as e:
            self.mostrar_dialogo_error_Login(f"Error en la base de datos: {e}")

    def mostrar_dialogo_error_Login(self, mensaje):
        dialogo = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Error",
        )
        dialogo.format_secondary_text(mensaje)
        dialogo.run()
        dialogo.destroy()

    def on_btnAceptar_clicked(self, widget, ventana_a_ocultar):
        conBD = ConexionBD("Peluqueria.sqlite")
        conBD.conectaBD()
        conBD.creaCursor()

        # Crear nueva ventana
        nueva_ventana = Gtk.Window(title="Base de datos")
        nueva_ventana.set_default_size(1050, 400)
        nueva_ventana.set_resizable(False)

        color_azul = Gdk.RGBA()
        color_azul.parse('#4682B4')
        nueva_ventana.override_background_color(Gtk.StateFlags.NORMAL, color_azul)

        # Caja principal vertical
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox.override_background_color(Gtk.StateFlags.NORMAL, color_azul)
        nueva_ventana.add(vbox)

        # Encabezado
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        header_box.override_background_color(Gtk.StateFlags.NORMAL, color_azul)
        imagen1 = Gtk.Image.new_from_file("/home/dam/PycharmProjects/Peluqueria/Imagenes/logoBase.png")
        imagen1.set_halign(Gtk.Align.CENTER)
        header_box.pack_start(imagen1, True, True, 0)
        vbox.pack_start(header_box, False, False, 0)

        self.liststore = Gtk.ListStore(int, str, str, int, str, int, int)

        # Entry de búsqueda
        self.entry_busqueda = Gtk.Entry()
        self.entry_busqueda.set_placeholder_text("Buscar por nombre, apellidos o servicios")
        self.entry_busqueda.connect("changed", self.on_busqueda_cambiada)

        # Crear TreeView
        treeview = Gtk.TreeView(model=self.liststore)
        self.trvDetalleAlbara = treeview
        titulos = ["ID", "Nombre", "Apellidos", "HoraCita", "Servicios", "Total_Gastado", "id_Peluquera"]
        for i, columna_titulo in enumerate(titulos):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(columna_titulo, renderer, text=i)
            treeview.append_column(column)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)
        scrolled_window.add(treeview)

        # Caja izquierda vertical
        caja_izquierda = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        caja_izquierda.override_background_color(Gtk.StateFlags.NORMAL, color_azul)
        caja_izquierda.pack_start(self.entry_busqueda, False, False, 5)
        caja_izquierda.pack_start(scrolled_window, True, True, 0)

        # Caja derecha
        derecha_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        derecha_box.override_background_color(Gtk.StateFlags.NORMAL, color_azul)

        formulario_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        formulario_box.override_background_color(Gtk.StateFlags.NORMAL, color_azul)
        derecha_box.set_valign(Gtk.Align.CENTER)  # <-- Aquí está la clave

        derecha_box.pack_start(formulario_box, True, True, 0)

        labels = ["Nombre", "Apellidos", "Hora Cita", "Servicios", "Total Gastado", "ID Peluquera"]
        self.entries = []

        for texto in labels:
            fila = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            fila.override_background_color(Gtk.StateFlags.NORMAL, color_azul)

            label = Gtk.Label(label=texto)
            label.set_halign(Gtk.Align.START)
            label.set_valign(Gtk.Align.CENTER)
            label.set_size_request(120, -1)
            label.override_background_color(Gtk.StateFlags.NORMAL, color_azul)

            entry = Gtk.Entry()
            entry.set_size_request(-1, 30)
            entry.set_valign(Gtk.Align.CENTER)

            fila.pack_start(label, False, False, 5)
            fila.pack_start(entry, True, True, 5)

            formulario_box.pack_start(fila, False, False, 0)
            self.entries.append(entry)

        botones_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        botones_box.override_background_color(Gtk.StateFlags.NORMAL, color_azul)

        botonAgregar = Gtk.Button(label="Agregar")
        botonBorrar = Gtk.Button(label="Borrar")
        botonEditar = Gtk.Button(label="Editar")
        botonRecargar = Gtk.Button(label="Recargar")
        boton_factura = Gtk.Button(label="Crear Factura PDF")


        botones_box.pack_start(botonAgregar, False, False, 0)
        botones_box.pack_start(botonBorrar, False, False, 0)
        botones_box.pack_start(botonEditar, False, False, 0)
        botones_box.pack_start(botonRecargar, False, False, 0)
        botones_box.pack_start(boton_factura, False, False, 0)

        botonAgregar.connect("clicked", self.on_btnAgregar_clicked)
        botonBorrar.connect("clicked", self.on_btnBorrar_clicked)
        botonEditar.connect("clicked", self.on_btnEditar_clicked)
        botonRecargar.connect("clicked", self.on_btnAceptar_clicked, nueva_ventana)
        boton_factura.connect("clicked", self.on_btnCrearFactura_clicked)

        botones_confirmacion_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        botonConfirmar = Gtk.Button(label="Confirmar")
        botonCancelar = Gtk.Button(label="Cancelar")

        botones_confirmacion_box.pack_start(botonConfirmar, False, False, 0)
        botones_confirmacion_box.pack_start(botonCancelar, False, False, 0)

        botonConfirmar.connect("clicked", self.on_btnConfirmar_clicked)
        botonCancelar.connect("clicked", self.on_btnCancelar_clicked)

        botones_box.pack_start(botones_confirmacion_box, False, False, 0)




        derecha_box.pack_start(formulario_box, True, True, 0)
        derecha_box.pack_start(botones_box, False, False, 0)


        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox.override_background_color(Gtk.StateFlags.NORMAL, color_azul)
        hbox.pack_start(caja_izquierda, True, True, 0)
        hbox.pack_start(derecha_box, False, False, 10)

        vbox.pack_start(hbox, True, True, 0)

        # Cargar datos iniciales
        self.cargar_datos_en_liststore()

        nueva_ventana.connect("destroy", Gtk.main_quit)
        nueva_ventana.show_all()
        ventana_a_ocultar.hide()

    def cargar_datos_en_liststore(self):
        self.liststore.clear()
        conBD = ConexionBD("Peluqueria.sqlite")
        conBD.conectaBD()
        conBD.creaCursor()
        conBD.cursor.execute(
            "SELECT Id, Nombre, Apellidos, HoraCita, Servicios, Total_Gastado, id_Peluquera FROM Clientes")

        for fila in conBD.cursor.fetchall():
            fila = list(fila)
            try:
                if isinstance(fila[3], str):
                    fila[3] = int(fila[3]) if fila[3].isdigit() else 0
            except:
                fila[3] = 0
            self.liststore.append(fila)

    def on_busqueda_cambiada(self, entry):
        texto = entry.get_text().lower()
        self.liststore.clear()

        conBD = ConexionBD("Peluqueria.sqlite")
        conBD.conectaBD()
        conBD.creaCursor()
        conBD.cursor.execute(
            "SELECT Id, Nombre, Apellidos, HoraCita, Servicios, Total_Gastado, id_Peluquera FROM Clientes")

        for fila in conBD.cursor.fetchall():
            fila = list(fila)
            nombre = str(fila[1]).lower()
            apellidos = str(fila[2]).lower()
            servicios = str(fila[4]).lower()

            if texto in nombre or texto in apellidos or texto in servicios or texto == "":
                try:
                    if isinstance(fila[3], str):
                        fila[3] = int(fila[3]) if fila[3].isdigit() else 0
                except:
                    fila[3] = 0
                self.liststore.append(fila)

    def realizar_agregado(self, widget):
        nombre = self.entries[0].get_text()
        apellidos = self.entries[1].get_text()
        hora_cita_str = self.entries[2].get_text()
        servicios = self.entries[3].get_text()
        total_gastado_str = self.entries[4].get_text()
        id_peluquera_str = self.entries[5].get_text()

        try:
            hora_cita = int(hora_cita_str)
        except ValueError:
            hora_cita = 0

        try:
            total_gastado = int(total_gastado_str)
        except ValueError:
            total_gastado = 0

        try:
            id_peluquera = int(id_peluquera_str)
        except ValueError:
            id_peluquera = 0

        # Insertar en la base de datos
        conBD = ConexionBD('Peluqueria.sqlite')
        conBD.conectaBD()
        conBD.creaCursor()

        conBD.engadeRexistro("""
            INSERT INTO Clientes (nombre, apellidos, HoraCita, servicios, total_gastado, id_peluquera)
            VALUES (?, ?, ?, ?, ?, ?)""",
                             nombre, apellidos, hora_cita, servicios, total_gastado, id_peluquera)

        conBD.pechaBD()

        self.liststore.append([None, nombre, apellidos, hora_cita, servicios, total_gastado, id_peluquera])

    def realizar_borrado(self, boton):
        seleccion = self.trvDetalleAlbara.get_selection()
        model, treeiter = seleccion.get_selected()

        if treeiter is not None:
            codigoProducto = model[treeiter][0]
            model.remove(treeiter)
            conBD = ConexionBD('Peluqueria.sqlite')
            conBD.conectaBD()
            conBD.creaCursor()
            conBD.borraRexistro("DELETE FROM Clientes WHERE Id = ?", codigoProducto)
            conBD.pechaBD()



    def realizar_edicion(self, widget):
        # Obtener la fila seleccionada
        seleccion = self.trvDetalleAlbara.get_selection()
        model, treeiter = seleccion.get_selected()

        if treeiter is not None:
            id_cliente = model[treeiter][0]

            nombre = self.entries[0].get_text()
            apellidos = self.entries[1].get_text()
            try:
                hora_cita = int(self.entries[2].get_text())
            except ValueError:
                hora_cita = 0
            servicios = self.entries[3].get_text()
            try:
                total_gastado = int(self.entries[4].get_text())
            except ValueError:
                total_gastado = 0
            try:
                id_peluquera = int(self.entries[5].get_text())
            except ValueError:
                id_peluquera = 0

            conBD = ConexionBD('Peluqueria.sqlite')
            conBD.conectaBD()
            conBD.creaCursor()

            conBD.actualizaRexistro("""
                UPDATE Clientes SET
                    Nombre = ?,
                    Apellidos = ?,
                    HoraCita = ?,
                    Servicios = ?,
                    Total_Gastado = ?,
                    id_Peluquera = ?
                WHERE Id = ?
            """, nombre, apellidos, hora_cita, servicios, total_gastado, id_peluquera, id_cliente)

            conBD.pechaBD()

            # Actualizar la fila
            model[treeiter][1] = nombre
            model[treeiter][2] = apellidos
            model[treeiter][3] = hora_cita
            model[treeiter][4] = servicios
            model[treeiter][5] = total_gastado
            model[treeiter][6] = id_peluquera
        else:
            print("No hay fila seleccionada para editar")

    def on_btnAgregar_clicked(self, widget):
        self.accion_actual = 'agregar'
        print("Preparado para AGREGAR. Complete los campos y presione Confirmar.")

    def on_btnEditar_clicked(self, widget):
        seleccion = self.trvDetalleAlbara.get_selection()
        model, treeiter = seleccion.get_selected()

        if treeiter is not None:
            self.operacion_actual = "editar"
            self.fila_seleccionada = treeiter

            valores = [str(model[treeiter][i]) for i in range(1, 7)]  # Del nombre al id_peluquera

            for entry, valor in zip(self.entries, valores):
                entry.set_text(valor)
        else:
            print("No hay fila seleccionada para editar.")

    def on_btnBorrar_clicked(self, widget):
        self.accion_actual = 'borrar'
        print("Preparado para BORRAR. Seleccione una fila y presione Confirmar.")

    def on_btnConfirmar_clicked(self, widget):
        if self.accion_actual == 'agregar':
            self.realizar_agregado(widget)
        elif self.accion_actual == 'editar':
            self.realizar_edicion(widget)
        elif self.accion_actual == 'borrar':
            self.realizar_borrado(widget)
        else:
            print("Ninguna operación preparada.")
        self.accion_actual = None
        self.limpiar_campos()

    def on_btnCancelar_clicked(self, widget):
        print("Operación cancelada.")
        self.accion_actual = None
        self.limpiar_campos()

    def limpiar_campos(self):
        for entry in self.entries:
            entry.set_text("")

    def enlace_activado(self, widget, uri):
        print(f"Enlace activado: {uri}")
        webbrowser.open(uri)

    def crear_factura_pdf(self, nombre_cliente, lista_items, total_factura, nombre_archivo="factura.pdf"):


        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Factura Peluquería", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Cliente: {nombre_cliente}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="L")
        pdf.ln(10)

        # Cabecera de tabla
        pdf.cell(80, 10, "Descripción", 1)
        pdf.cell(30, 10, "Cantidad", 1)
        pdf.cell(40, 10, "Precio Unitario", 1)
        pdf.cell(40, 10, "Subtotal", 1)
        pdf.ln()

        # Cuerpo de tabla
        for item in lista_items:
            descripcion = item.get('descripcion', '')
            cantidad = item.get('cantidad', 1)
            precio_unitario = float(item.get('precio_unitario', 0))
            subtotal = cantidad * precio_unitario

            pdf.cell(80, 10, descripcion, 1)
            pdf.cell(30, 10, str(cantidad), 1, align="C")
            pdf.cell(40, 10, f"{precio_unitario:.2f}", 1, align="R")
            pdf.cell(40, 10, f"{subtotal:.2f}", 1, align="R")
            pdf.ln()

        # Total
        pdf.cell(150, 10, "Total", 1)
        pdf.cell(40, 10, f"{total_factura:.2f}", 1, align="R")

        pdf.output(nombre_archivo)
        print(f"Factura PDF creada: {nombre_archivo}")

    def on_btnCrearFactura_clicked(self, widget):
        import datetime
        from fpdf import FPDF

        #Obtener cliente
        selection = self.trvDetalleAlbara.get_selection()
        model, treeiter = selection.get_selected()

        if not treeiter:
            print("Ningún cliente seleccionado.")
            return

        id_cliente = model[treeiter][0]  # Suponemos que la primera columna del TreeView es el ID

        conBD = ConexionBD('Peluqueria.sqlite')
        conBD.conectaBD()
        conBD.creaCursor()

        #Obtener nombre y apellidos del cliente
        consulta_cliente = "SELECT Nombre, Apellidos FROM Clientes WHERE Id = ?"
        resultado_cliente = conBD.consultaConParametros(consulta_cliente, id_cliente)

        if not resultado_cliente:
            print("No se encontró el cliente.")
            conBD.pechaBD()
            return

        nombre, apellidos = resultado_cliente[0]
        nombre_cliente = f"{nombre} {apellidos}"

        #Obtener detalles de las citas (hora, servicio, precio)
        consulta_citas = """
                         SELECT C.HoraCita, Servicios, Total_Gastado
                         FROM Clientes C
                         WHERE Id = ? \
                         """
        resultado_citas = conBD.consultaConParametros(consulta_citas, id_cliente)

        if not resultado_citas:
            print("No se encontraron citas para ese cliente.")
            conBD.pechaBD()
            return

        lista_items = []
        for fila in resultado_citas:
            hora_cita, servicio, precio_total = fila
            lista_items.append({
                'hora_cita': hora_cita,
                'descripcion': servicio,
                'precio_total': float(precio_total) if precio_total else 0.0
            })

        conBD.pechaBD()

        #Crear PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Factura Peluquería", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Cliente: {nombre_cliente}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="L")
        pdf.ln(10)

        pdf.cell(80, 10, "Hora de la Cita", 1)
        pdf.cell(60, 10, "Servicio", 1)
        pdf.cell(40, 10, "Precio Total", 1)
        pdf.ln()

        total = 0
        for item in lista_items:
            pdf.cell(80, 10, str(item['hora_cita']), 1)
            pdf.cell(60, 10, item['descripcion'], 1)
            pdf.cell(40, 10, f"{item['precio_total']:.2f}", 1, align="R")
            pdf.ln()
            total += item['precio_total']

        pdf.cell(140, 10, "Total", 1)
        pdf.cell(40, 10, f"{total:.2f}", 1, align="R")

        nombre_archivo = f"factura_cliente_{id_cliente}.pdf"
        pdf.output(nombre_archivo)
        print(f"Factura creada: {nombre_archivo}")

    def registro(self, widget, uri):
        if uri == "abrir_ventana":
            nueva_ventana = Gtk.Window(title="Registro")
            nueva_ventana.set_default_size(800, 450)
            nueva_ventana.set_resizable(False)

            # Contenedor horizontal principal
            contenedor_principal = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            nueva_ventana.add(contenedor_principal)

            # Cuadro izquierdo
            cuadro_izquierdo = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            cuadro_izquierdo.set_size_request(300, 450)

            color_izq = Gdk.RGBA()
            color_izq.parse('#FFFFFF')
            cuadro_izquierdo.override_background_color(Gtk.StateFlags.NORMAL, color_izq)

            imagen = Gtk.Image.new_from_file("/home/dam/PycharmProjects/Peluqueria/Imagenes/Logo.png")

            texto = "<a href='http://www.ejemplo.com'>Nuestra página</a>"
            lbl_enlace = Gtk.Label(label=texto)
            lbl_enlace.set_use_markup(True)
            lbl_enlace.connect("activate-link", self.enlace_activado)

            cuadro_izquierdo.pack_start(imagen, True, True, 20)
            cuadro_izquierdo.pack_start(lbl_enlace, False, False, 10)

            # Cuadro derecho
            cuadro_derecho = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
            cuadro_derecho.set_valign(Gtk.Align.CENTER)
            cuadro_derecho.set_halign(Gtk.Align.CENTER)
            cuadro_derecho.set_size_request(500, 450)

            color_der = Gdk.RGBA()
            color_der.parse('#4682B4')
            cuadro_derecho.override_background_color(Gtk.StateFlags.NORMAL, color_der)

            lbl_nombre = Gtk.Label(label="Nombre de usuario")
            lbl_nombre.set_halign(Gtk.Align.CENTER)
            self.txtNombre = Gtk.Entry()
            self.txtNombre.set_width_chars(25)
            self.txtNombre.set_halign(Gtk.Align.CENTER)

            lbl_contraseña = Gtk.Label(label="Contraseña del usuario")
            lbl_contraseña.set_halign(Gtk.Align.CENTER)
            self.txtContraseña = Gtk.Entry()
            self.txtContraseña.set_visibility(False)
            self.txtContraseña.set_width_chars(25)
            self.txtContraseña.set_halign(Gtk.Align.CENTER)

            lbl_email = Gtk.Label(label="Email")
            lbl_email.set_halign(Gtk.Align.CENTER)
            self.txtEmail = Gtk.Entry()
            self.txtEmail.set_width_chars(25)
            self.txtEmail.set_halign(Gtk.Align.CENTER)

            btn_aceptar = Gtk.Button(label="Aceptar")
            btn_aceptar.connect("clicked", self.on_registro_aceptar_clicked)

            texto_volver = "<a href='volver_login'>Volver al login</a>"
            lbl_volver = Gtk.Label(label=texto_volver)
            lbl_volver.set_use_markup(True)
            lbl_volver.connect("activate-link", self.volver_al_login)

            grid_formulario = Gtk.Grid()
            grid_formulario.set_row_spacing(10)
            grid_formulario.set_column_spacing(10)
            grid_formulario.set_column_homogeneous(False)
            grid_formulario.set_valign(Gtk.Align.CENTER)
            grid_formulario.set_halign(Gtk.Align.CENTER)

            formulario = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            formulario.set_valign(Gtk.Align.CENTER)
            formulario.set_halign(Gtk.Align.CENTER)

            box_nombre = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            box_nombre.pack_start(lbl_nombre, False, False, 0)
            box_nombre.pack_start(self.txtNombre, False, False, 0)

            box_contraseña = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            box_contraseña.pack_start(lbl_contraseña, False, False, 0)
            box_contraseña.pack_start(self.txtContraseña, False, False, 0)

            box_email = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            box_email.pack_start(lbl_email, False, False, 0)
            box_email.pack_start(self.txtEmail, False, False, 0)

            formulario.pack_start(box_nombre, False, False, 0)
            formulario.pack_start(box_contraseña, False, False, 0)
            formulario.pack_start(box_email, False, False, 0)
            formulario.pack_start(btn_aceptar, False, False, 10)
            formulario.pack_start(lbl_volver, False, False, 5)

            cuadro_derecho.pack_start(formulario, True, True, 10)

            contenedor_principal.pack_start(cuadro_izquierdo, False, False, 0)
            contenedor_principal.pack_start(cuadro_derecho, True, True, 0)

            nueva_ventana.show_all()
            self.hide()

            return True
        return False

    def volver_al_login(self, widget, uri):
        if uri == "volver_login":
            widget.get_toplevel().destroy()
            self.ventana_login.show_all()
            return True
        return False

    def mostrar_dialogo_error(self, ventana, mensaje):
            dialogo = Gtk.MessageDialog(
                transient_for=ventana,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CLOSE,
                text=mensaje
            )
            dialogo.run()
            dialogo.destroy()

    def on_registro_aceptar_clicked(self, widget):
            nombre = self.txtNombre.get_text().strip()
            contraseña = self.txtContraseña.get_text().strip()
            email = self.txtEmail.get_text().strip()

            ventana = widget.get_toplevel()

            if not nombre or not contraseña or not email:
                self.mostrar_dialogo_error(ventana, "Todos los campos son obligatorios.")
                return

            try:
                conexion = sqlite3.connect("Peluqueria.sqlite")
                cursor = conexion.cursor()

                cursor.execute("SELECT * FROM Usuarios WHERE nombre = ?", (nombre,))
                if cursor.fetchone():
                    self.mostrar_dialogo_error(ventana, f"El nombre de usuario '{nombre}' ya está en uso.")
                    conexion.close()
                    return

                cursor.execute("INSERT INTO Usuarios (nombre, contraseña, correo) VALUES (?, ?, ?)",
                               (nombre, contraseña, email))
                conexion.commit()
                conexion.close()

                print("Usuario registrado correctamente.")
                ventana.destroy()
                self.show_all()

            except Exception as e:
                self.mostrar_dialogo_error(ventana, f"Error al registrar usuario: {e}")


if __name__ == "__main__":
    ventana = FiestraPrincipal()
    ventana.connect("destroy", Gtk.main_quit)
    ventana.show_all()
    Gtk.main()
