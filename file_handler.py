from tkinter import *
import pandas as pd
import csv
import os
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog

class DataManager:
    def __init__(self):
        self.df_file = None
        self.columnas = None
        self.df_assays = None
        self.df_survey = None
        self.df_collar = None
        

    def detectar_delimitador(self, filepath):
        with open(filepath, "r") as file:
            line = file.readline()
            if ";" in line:
                return ";"
            else:
                return ","

    def cargar_archivo(self, filepath, nombre_archivo):
       
        """Función para cargar y procesar el archivo assays.csv"""
        filepath = filedialog.askopenfilename(title=f"Cargar {nombre_archivo}.csv",
                                              filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*"))
                                             )
        if not filepath:
            return None, None, None
        
        # Detectar el delimitador correcto
        delimiter = self.detectar_delimitador(filepath)
    
        # Utiliza Pandas para leer el archivo CSV.
        df_file = pd.read_csv(filepath, delimiter=delimiter)
        filename = os.path.basename(filepath)

        # Almacena el DataFrame en la propiedad adecuada
        if nombre_archivo.upper() == 'ASSAYS':
            self.df_assays = df_file
        elif nombre_archivo.upper() == 'SURVEY':
            self.df_survey = df_file
        elif nombre_archivo.upper() == 'COLLAR':
            self.df_collar = df_file

        columnas = df_file.columns.tolist()

        return df_file, columnas, filename
    
    def view_files(self, root, df_file, columnas, filename):
        # Crear una nueva ventana Toplevel
        top = Toplevel(root)
        top.title(f"Visualizar {filename}")
        top.geometry("600x400")
        top.minsize(600, 400)

        contenedor = ttk.Frame(top)
        contenedor.pack(fill='both', expand=True)

        # Crear el Treeview
        tree = ttk.Treeview(contenedor, columns=columnas)

        # Configurar la barra de desplazamiento
        scrollbar_vertical = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
        scrollbar_horizontal = ttk.Scrollbar(tree, orient="horizontal", command=tree.xview)

        tree.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)
        tree.column("#0", width=50, stretch=NO)  # Columna fantasma
        for col in columnas:
            tree.column(col, anchor=CENTER, width=100, stretch=NO)
            tree.heading(col, text=col.capitalize())

        # Agregar nuestros datos al treeview
        for index, fila in df_file.iterrows():
            tree.insert(parent='', index='end', text=str(index+1), values=fila.tolist())

        # Empaquetar el treeview finalmente
        tree.pack(side="left", fill="both", expand=True)
        scrollbar_vertical.pack(side="right", fill="y")
        scrollbar_horizontal.pack(side='bottom', fill='x')

    def get_df_assays(self):
        return self.df_assays

    def get_df_survey(self):
        return self.df_survey

    def get_df_collar(self):
        return self.df_collar    
    