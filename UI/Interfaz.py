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
        # Crear conexión y cursor a la base de datos
        conBD = ConexionBD("Peluqueria.sqlite")
        conBD.conectaBD()
        conBD.creaCursor()

        # Crear nueva ventana
        nueva_ventana = Gtk.Window(title="Base de datos")
        nueva_ventana.set_default_size(900, 500)

        # Caja principal vertical
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        nueva_ventana.add(vbox)

        # --- Encabezado personalizado encima del TreeView ---
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        imagen1 = Gtk.Image.new_from_file("/home/dam/PycharmProjects/Peluqueria/Imagenes/Logo.png")
        header_box.pack_start(imagen1, False, False, 5)
        vbox.pack_start(header_box, False, False, 0)

        # Crear modelo ListStore y asignarlo a self
        self.liststore = Gtk.ListStore(int, str, str, int, str, int, int)
        conBD.cursor.execute(
            "SELECT Id, Nombre, Apellidos, HoraCita, Servicios, Total_Gastado, id_Peluquera FROM Clientes")
        for fila in conBD.cursor.fetchall():
            fila = list(fila)
            try:
                if isinstance(fila[3], str):
                    fila[3] = int(fila[3]) if fila[3].isdigit() else 0
            except Exception as e:
                print(f"Error convirtiendo fila {fila}: {e}")
                fila[3] = 0  # valor por defecto si falla la conversión

            self.liststore.append(fila)  # Usar self.liststore

        # Crear TreeView con el modelo
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

        # Caja horizontal para el contenido principal
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox.pack_start(scrolled_window, True, True, 0)

        # --- Caja derecha: formulario + botones ---
        derecha_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        # Caja del formulario
        formulario_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        labels = ["Nombre", "Apellidos", "Hora Cita", "Servicios", "Total Gastado", "ID Peluquera"]
        self.entries = []

        for texto in labels:
            label = Gtk.Label(label=texto, halign=Gtk.Align.START)
            entry = Gtk.Entry()
            fila = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            fila.pack_start(label, False, False, 5)
            fila.pack_start(entry, True, True, 5)
            formulario_box.pack_start(fila, False, False, 0)
            self.entries.append(entry)

        # Caja de botones
        botones_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        botonAgregar = Gtk.Button(label="Agregar")
        botonBorrar = Gtk.Button(label="Borrar")
        botonEditar = Gtk.Button(label="Editar")

        botones_box.pack_start(botonAgregar, False, False, 0)
        botones_box.pack_start(botonBorrar, False, False, 0)
        botones_box.pack_start(botonEditar, False, False, 0)

        botonAgregar.connect("clicked", self.on_btnAgregar_clicked)
        botonBorrar.connect("clicked", self.on_btnBorrar_clicked)
        botonEditar.connect("clicked", self.on_btnEditar_clicked)

        boton_factura = Gtk.Button(label="Crear Factura PDF")
        boton_factura.connect("clicked", self.on_btnCrearFactura_clicked)

        # Añádelo a la caja o layout que tengas en la ventana
        # Por ejemplo, si tienes un box llamado 'botones_box':
        botones_box.pack_start(boton_factura, False, False, 0)

        # Añadir formulario y botones juntos
        derecha_box.pack_start(formulario_box, True, True, 0)
        derecha_box.pack_start(botones_box, False, False, 0)

        # Añadir a hbox principal
        hbox.pack_start(derecha_box, False, False, 10)

        # Añadir hbox completo al vbox principal
        vbox.pack_start(hbox, True, True, 0)

        # Mostrar ventana y ocultar la anterior
        nueva_ventana.connect("destroy", Gtk.main_quit)
        nueva_ventana.show_all()
        ventana_a_ocultar.hide()

    def on_btnAgregar_clicked(self, widget):
        nombre = self.entries[0].get_text()
        apellidos = self.entries[1].get_text()
        hora_cita_str = self.entries[2].get_text()
        servicios = self.entries[3].get_text()
        total_gastado_str = self.entries[4].get_text()
        id_peluquera_str = self.entries[5].get_text()

        # Validaciones y conversiones
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

        # Insertar en el liststore de la interfaz
        self.liststore.append([None, nombre, apellidos, hora_cita, servicios, total_gastado, id_peluquera])

    def on_btnBorrar_clicked(self, boton):
        seleccion = self.trvDetalleAlbara.get_selection()
        model, treeiter = seleccion.get_selected()

        if treeiter is not None:
            codigoProducto = model[treeiter][0]
            dialog = Gtk.MessageDialog(self, Gtk.DialogFlags.MODAL, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, "¿Seguro que quieres borrar este producto?")
            response = dialog.run()

            if response == Gtk.ResponseType.YES:
                model.remove(treeiter)  # Eliminar de la vista
                conBD = ConexionBD('Peluqueria.sqlite')
                conBD.conectaBD()
                conBD.creaCursor()
                conBD.borraRexistro("DELETE FROM Clientes WHERE Id = ?",
                                     codigoProducto)
                conBD.pechaBD()
            dialog.destroy()
        else:
            print("No se ha seleccionado ningún detalle para borrar.")

    def on_btnEditar_clicked(self, widget):
        # Obtener la fila seleccionada
        seleccion = self.trvDetalleAlbara.get_selection()
        model, treeiter = seleccion.get_selected()

        if treeiter is not None:
            id_cliente = model[treeiter][0]  # Asumiendo que ID está en columna 0

            # Obtener valores actualizados desde las entradas
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

            # Conectar a BD y actualizar registro
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

            # Actualizar la fila en el ListStore
            model[treeiter][1] = nombre
            model[treeiter][2] = apellidos
            model[treeiter][3] = hora_cita
            model[treeiter][4] = servicios
            model[treeiter][5] = total_gastado
            model[treeiter][6] = id_peluquera
        else:
            print("No hay fila seleccionada para editar")

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

        # Paso 1: Obtener cliente seleccionado del TreeView
        selection = self.trvDetalleAlbara.get_selection()
        model, treeiter = selection.get_selected()

        if not treeiter:
            print("Ningún cliente seleccionado.")
            return

        id_cliente = model[treeiter][0]  # Suponemos que la primera columna del TreeView es el ID

        # Paso 2: Conectar con la base de datos
        conBD = ConexionBD('Peluqueria.sqlite')
        conBD.conectaBD()
        conBD.creaCursor()

        # Paso 3: Obtener nombre y apellidos del cliente
        consulta_cliente = "SELECT Nombre, Apellidos FROM Clientes WHERE Id = ?"
        resultado_cliente = conBD.consultaConParametros(consulta_cliente, id_cliente)

        if not resultado_cliente:
            print("No se encontró el cliente.")
            conBD.pechaBD()
            return

        nombre, apellidos = resultado_cliente[0]
        nombre_cliente = f"{nombre} {apellidos}"

        # Paso 4: Obtener detalles de las citas (hora, servicio, precio)
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

        # Paso 5: Crear PDF
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
            self.txtNombre = Gtk.Entry()
            self.txtNombre.set_width_chars(20)
            self.txtNombre.set_halign(Gtk.Align.CENTER)
            caja_nombre.pack_start(lblNombre, False, False, 0)
            caja_nombre.pack_start(self.txtNombre, False, False, 0)

            # Campo contraseña
            lblContraseña = Gtk.Label(label="Contraseña del usuario")
            lblContraseña.set_halign(Gtk.Align.CENTER)
            self.txtContraseña = Gtk.Entry()
            self.txtContraseña.set_visibility(False)
            self.txtContraseña.set_width_chars(20)
            self.txtContraseña.set_halign(Gtk.Align.CENTER)
            caja_nombre.pack_start(lblContraseña, False, False, 0)
            caja_nombre.pack_start(self.txtContraseña, False, False, 0)


            lblEmail = Gtk.Label(label="Email")
            lblEmail.set_halign(Gtk.Align.CENTER)
            self.txtEmail = Gtk.Entry()
            self.txtEmail.set_width_chars(20)
            self.txtEmail.set_halign(Gtk.Align.CENTER)
            caja_nombre.pack_start(lblEmail, False, False, 0)
            caja_nombre.pack_start(self.txtEmail, False, False, 0)

            btnAceptar = Gtk.Button(label="Aceptar")
            btnAceptar.connect("clicked", self.on_registro_aceptar_clicked)

            caja_nombre.pack_start(btnAceptar, False, False, 0)

            cuadro_nueva.pack_start(cuadro1, False, False, 10)
            cuadro_nueva.pack_start(caja_nombre, False, False, 10)

            # Mostrar ventana y ocultar la principal
            nueva_ventana.show_all()
            self.hide()

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
