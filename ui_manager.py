import pandas as pd
from tkinter import *
from tkinter import ttk
from tkmacosx import Button
from tooltips import createToolTip
from help import *
from file_handler import DataManager
from data_processor import DataProcessor
import plotly.graph_objects as go
from utils import resource_path


logo_path = resource_path("logo.png")
data_manager = DataManager()
data_processor = DataProcessor(data_manager)

def mostrar_ventana_principal():
    def update_info(text):
        info_panel.config(text=text)

    def cargar_archivo(tipo_archivo):
        update_info(f"Cargando archivo {tipo_archivo}...")
        df, col, filename = data_manager.cargar_archivo(filepath=None, nombre_archivo=tipo_archivo.upper())
        if filename:
            data_manager.view_files(root, df, col, filename)
            update_info(f"Archivo {filename} cargado con éxito")
        else:
            update_info("Carga de archivo cancelada.")

    def solicitar_parametros_composite():
        top = Toplevel(root)
        top.title("Parámetros de Composite")

        # Etiqueta para la entrada del intervalo de composito
        etiqueta_intervalo = Label(top, text="Ingrese la longitud del intervalo de composito:")
        etiqueta_intervalo.pack(pady=(10, 0))  # Espaciado superior

        # Entrada para el intervalo de composito
        entrada_intervalo = Entry(top)
        entrada_intervalo.pack(pady=10)

        # Función para manejar el cálculo al hacer clic en el botón
        def manejar_calculo_composito():
            try:
                # Intenta convertir el texto de la entrada a un número flotante
                intervalo_composito = float(entrada_intervalo.get())
                # Llama a la función de procesamiento con el valor de intervalo
                df_compositado, filename = data_processor.realizar_composito(intervalo_composito)
                
            except ValueError:
                # Maneja el error si el valor ingresado no es un número
                print("Por favor, ingrese un número válido para el intervalo de composito.")
                # Puedes mostrar un mensaje de error en la interfaz aquí
            col = df_compositado.columns.tolist()    
            data_manager.view_files(root, df_compositado, col, filename)
        boton_calcular = ttk.Button(top, text="Calcular Composite", command=manejar_calculo_composito)
        boton_calcular.pack(pady=10)
            
    def View3d_samples():
        df_comp_coord = data_processor.calculate_sample_coordinates()
        if df_comp_coord is not None:
            # Aquí podrías hacer la visualización 3D con df_comp_coord
            #print(df_comp_coord)    
            data_processor.Plot_samples3d(df_comp_coord)
        else:
            print("Error al obtener las coordenadas del compositado.")


    root = Tk()
    root.configure(background='#333333')
    root.title('MapComp')
    root.geometry('500x500')

    style = ttk.Style()
    style.configure("Custom.TButton",  background='#333333', foreground='#000', width=20, font=('Helvetica', 11))

    info_panel = Label(root, text=f"{help_upload}", anchor="w", justify="left", bg="lightgray")
    info_panel.pack(side="left", fill="y")

    frame = Frame(root)
    frame.configure(background='#333333')
    frame.pack(side="right", expand=True)

    btn = ttk.Button(frame, text="Upload Assay", style="Custom.TButton",  command=lambda: cargar_archivo('assays'))
    btn.pack(pady=10)
    createToolTip(btn, 'Subir Archivo Assays.csv')

    btn1 = ttk.Button(frame, text="Upload Survey", style="Custom.TButton", command=lambda: cargar_archivo('survey'))
    btn1.pack(pady=10)
    createToolTip(btn1, 'Subir Archivo Survey.csv')

    btn2 = ttk.Button(frame, text="Upload Collar", style="Custom.TButton", command=lambda: cargar_archivo('collar'))
    btn2.pack(pady=10)
    createToolTip(btn2, 'Subir Archivo Collar.csv')

    btn3 = ttk.Button(frame, text="Composite", style="Custom.TButton", command=solicitar_parametros_composite)
    btn3.pack(pady=10)
    createToolTip(btn3, 'Calcula el composito')

    btn4 = ttk.Button(frame, text="View 3D", style="Custom.TButton", command=View3d_samples)
    btn4.pack(pady=10)
    createToolTip(btn4, 'Visualizar los sondajes compositados')

    root.mainloop()

def mostrar_ventana_bienvenida():
    ventana_bienvenida = Tk()
    ventana_bienvenida.title("Bienvenido a MapComp")
    
    # Dimensiones de la ventana
    ventana_ancho = 600
    ventana_alto = 400
    
    # Obtiene las dimensiones de la pantalla
    pantalla_ancho = ventana_bienvenida.winfo_screenwidth()
    pantalla_alto = ventana_bienvenida.winfo_screenheight()
    
    # Calcula la posición x e y para centrar la ventana
    x = (pantalla_ancho / 2) - (ventana_ancho / 2)
    y = (pantalla_alto / 2) - (ventana_alto / 2)
    
    # Establece la geometría de la ventana con las nuevas coordenadas
    ventana_bienvenida.geometry('%dx%d+%d+%d' % (ventana_ancho, ventana_alto, x, y))

     # Marco para el logo
    frame_logo = Frame(ventana_bienvenida)
    frame_logo.pack(fill="both", expand=True)
    
        
    # Suponiendo que tienes un logo.png en el directorio actual. Cambia la ruta según sea necesario.
    logo = PhotoImage(file=logo_path)  # Asegúrate de ajustar esta ruta
    label_logo = Label(frame_logo, image=logo)
    label_logo.image = logo
    label_logo.pack()
    
    copyrigh = Label(frame_logo, text="© 2024 Desarrollado por Juan Carlos Yepez C.", bg="lightgray")
    copyrigh.place(relx=0.5, rely=0.65, anchor="center")
    
    # Cierra la ventana de bienvenida después de 5 segundos y muestra la ventana principal
    ventana_bienvenida.after(5000, lambda: [ventana_bienvenida.destroy(), mostrar_ventana_principal()])
    
    ventana_bienvenida.mainloop()

# Llamada inicial a la ventana de bienvenida
mostrar_ventana_bienvenida()