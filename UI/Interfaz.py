import gi

gi.require_version('Gtk', '3.0')  # Especificamos la versión de GTK
from gi.repository import Gtk, Gdk


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
        cuadro1.pack_start(imagen1, True, True, 0)

        cuadro2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        cuadro2.set_size_request(400, 400)
        color2 = Gdk.RGBA()
        color2.parse('#4682B4')
        cuadro2.override_background_color(Gtk.StateFlags.NORMAL, color2)

        lblNombre = Gtk.Label(label="Nombre de usuario")
        self.txtNombre = Gtk.Entry()

        self.txtNombre.set_size_request(80, 1)
        self.txtNombre.set_halign(Gtk.Align.CENTER)
        self.txtNombre.set_valign(Gtk.Align.CENTER)

        lblContraseña = Gtk.Label(label="Contraseña del usuario")
        self.txtContraseña = Gtk.Entry()
        self.txtContraseña.set_visibility(False)

        self.txtContraseña.set_size_request(80, 1)
        self.txtContraseña.set_halign(Gtk.Align.CENTER)
        self.txtContraseña.set_valign(Gtk.Align.CENTER)

        self.txtNombre.set_vexpand(True)
        self.txtContraseña.set_vexpand(True)

        cuadro2.pack_start(lblNombre, False, False, 0)
        cuadro2.pack_start(self.txtNombre, False, False, 0)
        cuadro2.pack_start(lblContraseña, False, False, 0)
        cuadro2.pack_start(self.txtContraseña, False, False, 0)

        grid = Gtk.Grid()
        grid.add(cuadro2)

        caja_horizontal.pack_start(cuadro1, True, True, 0)
        caja_horizontal.pack_start(grid, True, True, 0)


if __name__ == "__main__":
    ventana = FiestraPrincipal()
    ventana.connect("destroy", Gtk.main_quit)
    ventana.show_all()
    Gtk.main()
