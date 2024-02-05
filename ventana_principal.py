import tkinter as tk
from tkinter import Toplevel, PhotoImage

# Función para cerrar la ventana de bienvenida y abrir la ventana principal
def abrir_ventana_principal():
    ventana_bienvenida.destroy()  # Cierra la ventana de bienvenida
    # Aquí deberías colocar el código para abrir tu ventana principal
    ventana_principal = tk.Tk()
    ventana_principal.title("Ventana Principal")
    ventana_principal.geometry("400x400")
    tk.Label(ventana_principal, text="Esta es la ventana principal de la aplicación").pack()
    ventana_principal.mainloop()

# Crear la ventana de bienvenida
ventana_bienvenida = tk.Tk()
ventana_bienvenida.title("Bienvenido")
ventana_bienvenida.geometry("600x400")

# Cargar y mostrar el logo
logo = PhotoImage(file="C:\Users\JUANC\00_MAESTRIA VIU\DESARROLLO_TFM\MapComp\logo.jpg")  # Asegúrate de poner la ruta correcta a tu archivo de logo
label_logo = tk.Label(ventana_bienvenida, image=logo)
label_logo.pack()

# Mostrar el texto de copyright
copyrigh = tk.Label(ventana_bienvenida, text="© 2024 Tu Compañía. Todos los derechos reservados.")
copyrigh.pack(side="bottom")

# Configurar temporizador para cerrar la ventana de bienvenida y abrir la ventana principal
ventana_bienvenida.after(5000, abrir_ventana_principal)  # 5000 milisegundos = 5 segundos

ventana_bienvenida.mainloop()
