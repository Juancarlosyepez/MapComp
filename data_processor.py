
import pandas as pd
import numpy as np
import math
from file_handler import DataManager
import plotly.graph_objects as go

data_manager = DataManager()
class DataProcessor:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.df_compositado = None  # Añade esto
        self.df_comp_coord = None
        self.filename = None

    def procesar_datos(self, intervalos, intervalo_composito):
        # Accede a los DataFrames usando los métodos getter
        df_assays = self.data_manager.get_df_assays()

        # Aquí puedes comenzar a procesar los DataFrames
        # Por ejemplo, imprimir los primeros registros de cada uno
        if df_assays is not None:
            #print(df_assays.head())
            intervalo_actual = []
            composiciones_ponderadas = []
            tipos_de_roca = []
            last_to = None
            
            for i, fila in intervalos.iterrows():
                longitud = fila['To'] - fila['From']
                
                # Filtrar las columnas de composición para asegurarnos de que sean numéricas
                composicion_numerica = fila[3:].apply(pd.to_numeric, errors='coerce')
                
                if sum(intervalo_actual) + longitud <= intervalo_composito:
                    intervalo_actual.append(longitud)
                    composiciones_ponderadas.append(composicion_numerica * longitud)
                    tipos_de_roca.extend([fila['Litologia']] * int(math.ceil(longitud)))
                    last_to = fila['To']
                else:
                    if intervalo_actual:
                        tipos_contados = pd.Series(tipos_de_roca).value_counts()
                        if not tipos_contados.empty:  # Comprobar si hay valores en la serie
                            tipo_de_roca_seleccionado = tipos_contados.idxmax()
                        else:
                            tipo_de_roca_seleccionado = np.nan
                        composiciones_promedio = sum(composiciones_ponderadas) / sum(intervalo_actual)
                        resultado = [fila['DDH'], last_to,tipo_de_roca_seleccionado] + composiciones_promedio.tolist() 
                        yield resultado
                    intervalo_actual = [longitud]
                    composiciones_ponderadas = [composicion_numerica * longitud]
                    tipos_de_roca = [fila['Litologia']] * int(math.ceil(longitud))
                    last_to = fila['To']
                    
            if intervalo_actual:
                tipos_contados = pd.Series(tipos_de_roca).value_counts()
                if not tipos_contados.empty:  # Comprobar si hay valores en la serie
                    tipos_contados_invertidos = tipos_contados[::-1]
                    tipo_de_roca_seleccionado = tipos_contados_invertidos.idxmax()
                else:
                    tipo_de_roca_seleccionado = np.nan
                composiciones_promedio = sum(composiciones_ponderadas) / sum(intervalo_actual)
                resultado = [fila['DDH'], last_to, tipo_de_roca_seleccionado] + composiciones_promedio.tolist()
                yield resultado

    def realizar_composito(self, intervalo_composito):
        df = self.data_manager.get_df_assays()
        # Crear una lista para almacenar los resultados
        resultado = []

        # Iterar por cada grupo de taladro y compositar
        
        for taladro, intervalos in df.groupby('DDH'):
            resultado.extend(self.procesar_datos(intervalos, intervalo_composito))

        # Crear un DataFrame a partir de la lista de resultados
        columnas_resultado = ['DDH', 'To','Litologia'] + df.columns[3:].tolist()
        df_resultado = pd.DataFrame(resultado, columns=columnas_resultado)

        # Redondear valores a 3 decimales
        df_resultado = df_resultado.round(3)
        df_compositado = df_resultado.iloc[:,:-1]
        # Guardar el DataFrame resultante en un archivo CSV
        self.df_compositado = df_compositado
        self.filename = f'composito_{intervalo_composito}m.csv'
        

        #print(df_compositado)

        return df_compositado, self.filename

    def calculate_sample_coordinates(self):
    # Lógica para calcular coordenadas...
        df_comp = self.df_compositado
        df_survey = self.data_manager.get_df_survey()
        df_collar = self.data_manager.get_df_collar()
        
        # Inicializar variables para las coordenadas X, Y, Z y distancia acumulada L
        L_prev = 0

        # Calcular las coordenadas X, Y, Z y la distancia acumulada L para cada muestra
        for index, row in df_comp.iterrows():
            ddh = row['DDH']
            to_curr = row['To']
            
            # Obtener las coordenadas del collar del taladro correspondiente
            collar_coords = df_collar.loc[df_collar['HOLE-ID'] == ddh,
                                        ['ESTE_X', 'NORTE_Y', 'COTA_Z']].values[0]
            X_collar, Y_collar, Z_collar = collar_coords
            
            dip = df_survey.loc[df_survey['HOLE-ID'] == ddh, 'DIP'].values[0]
            azimuth = df_survey.loc[df_survey['HOLE-ID'] == ddh, 'AZIMUTH'].values[0]
            
            if L_prev == 0 or ddh != df_comp.loc[index - 1, 'DDH']:
                L = to_curr / 2
            else:
                L = L_prev + (to_curr - df_comp.loc[index - 1, 'To']) / 2
                
            X_curr = X_collar + L * np.cos(np.radians(dip)) * np.cos(np.radians(azimuth))
            Y_curr = Y_collar + L * np.cos(np.radians(dip)) * np.sin(np.radians(azimuth))
            Z_curr = Z_collar + L * np.sin(np.radians(dip))
            
            # Actualizar los valores previos para la siguiente iteración
            L_prev = to_curr

            # Asignar los valores de X, Y, Z para la muestra actual en el DataFrame
            df_comp.at[index, 'ESTE_X'] = X_curr
            df_comp.at[index, 'NORTE_Y'] = Y_curr
            df_comp.at[index, 'COTA_Z'] = Z_curr

            #self.df_comp_coord = df_comp

        # Mostrar el DataFrame resultante con las nuevas columnas X, Y, Z
        filename =  self.filename  
        #print(filename)
        print(df_comp.head())
        # Guardar el DataFrame fusionado con coordenadas en un nuevo archivo CSV
        df_comp.to_csv(filename, index=False, encoding='utf-8')
        return df_comp
    
    def Plot_samples3d(self, df):
        df_collar = self.data_manager.get_df_collar()
        
        # Obtener las coordenadas X, Y, Z de las muestras
        X_samples = df['ESTE_X']
        Y_samples = df['NORTE_Y']
        Z_samples = df['COTA_Z']

        # Obtener las coordenadas del collar de cada taladro
        collar_coords_unique = df_collar.drop_duplicates('HOLE-ID')[['HOLE-ID', 'ESTE_X', 'NORTE_Y', 'COTA_Z']]
        X_collar = collar_coords_unique['ESTE_X']
        Y_collar = collar_coords_unique['NORTE_Y']
        Z_collar = collar_coords_unique['COTA_Z']
        collar_labels = collar_coords_unique['HOLE-ID']


        # Colores para cada clase de litología
        litology_colors = {
            'MG': 'magenta',
            'INT': 'orange',
            'FLL': 'black',
            'SL': 'brown',
            'SK': 'green',
            'CZ': 'cyan',
            'MAR': 'Ivory'
        }

        # Crear una figura 3D interactiva
        fig = go.Figure()

        # Agregar el collar de los taladros al gráfico con etiquetas
        fig.add_trace(go.Scatter3d(
            x=X_collar,
            y=Y_collar,
            z=Z_collar,
            mode='markers+text',
            text=collar_labels,
            texttemplate='%{text}',
            textposition='bottom center',
            marker=dict(
                size=5,
                #color='black',
                #symbol='cross',  # Símbolo de cruz predeterminado
                symbol='circle-open',
                #symbol='diamond',
                #symbol='square',
                opacity=0.5,
                line=dict(color='black', width=1),
                #colorscale='Viridis',
                showscale=False,
            ),
            name='Collar del taladro',
            showlegend=False,  # No mostrar en la leyenda
        ))
        # Agregar otro trazo con cruces
        fig.add_trace(go.Scatter3d(
            x=X_collar,
            y=Y_collar,
            z=Z_collar,
            mode='markers+text',
            text=collar_labels,
            texttemplate='%{text}',
            textposition='bottom center',
            marker=dict(
                size=2,
                symbol='x',
                color='black',
                opacity=0.5,
                #line=dict(color='black', width=1),
            ),
            name='Collar del taladro',
            #showlegend=False,  # No mostrar en la leyenda
        ))

        clases_lito=df['Litologia'].unique()
        litology_classes = list(clases_lito)
        litology_classes
        # Agregar las muestras al gráfico, coloreando por tipo de litología
        for litology_class in litology_classes:
            fig.add_trace(go.Scatter3d(
                x=X_samples[df['Litologia'] == litology_class],
                y=Y_samples[df['Litologia'] == litology_class],
                z=Z_samples[df['Litologia'] == litology_class],
                mode='markers',
                marker=dict(
                    size=5,
                    color=litology_colors[litology_class],
                    #symbol='circle-open',
                    opacity=0.8,
                    #line=dict(color='black', width=1),
                ),
                name=litology_class,
            ))

        # Configurar el diseño del gráfico y agrandar la ventana de visualización
        fig.update_layout(
            scene=dict(
                xaxis_title='Este X',
                yaxis_title='Norte Y',
                zaxis_title='Elevacion Z'
            ),
            title='Ubicación de las muestras y collares de los taladros',
            width=1200,
            height=800,
            showlegend=True,
            legend=dict(
                x=0.9,
                y=0.9,
                itemsizing='constant'
            )
        )
        fig.write_html('muestra_y_collares_3d.html')

        # Mostrar el gráfico interactivo
        fig.show()
    
    def get_df_comp(self):
        return self.df_compositado
        # if df_survey is not None:
        #     print(df_survey.head())
        # if df_collar is not None:
        #     print(df_collar.head())

        




