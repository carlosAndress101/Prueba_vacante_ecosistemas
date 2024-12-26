from Class.email import EmailSendOutlook
from Class.data import DataLoader
from utils.formato_result import formatear_resultados
import pandas as pd
import os

class Comisiones:
    """Clase principal para calcular comisiones y enviar correos."""
    
    def __init__(self, directorio):
        self.directorio = directorio
        self.data_loader = DataLoader(directorio)
        self.parametros = self.data_loader.load_parameters()
        self.email_sender = EmailSendOutlook(self.parametros['client_id'], self.parametros['tenant_id'], self.parametros['mail_to'], self.parametros['password'])
    
    def load_data(self):
        """Carga los datos necesarios para la ejecución."""
        try:
            print("Leyendo datos desde la base de datos...")
            self.df_comisiones = self.data_loader.load_table_as_dataframe('commissions')
            self.df_descuentos = self.data_loader.load_table_as_dataframe('discounts')
            print("Datos cargados correctamente.")
            
            # Convertir fechas
            self.parametros['date_init'] = pd.to_datetime(self.parametros['date_init'], format='%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
            self.parametros['date_end'] = pd.to_datetime(self.parametros['date_end'], format='%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            raise
    
    def calculate_commissions(self):
        """Calcula las comisiones según los parámetros y contratos."""
        try:
            print("Calculando comisiones...")
            sql_query = self.data_loader.load_sql('count_call_api.sql', self.parametros)
            
            max_valor_succ = sql_query['successful_count'].max()
            max_valor_unsucc = sql_query['unsuccessful_count'].max()
            
            # Rellenar valores nulos con los valores máximos
            self.df_comisiones.fillna({'max_successful_requests': max_valor_succ}, inplace=True)
            self.df_descuentos.fillna({'max_unsuccessful_requests': max_valor_unsucc}, inplace=True)

            # Subir datos
            db_connection = self.data_loader.get_db_connection()
            sql_query.to_sql('csc', db_connection, if_exists='replace', index=False)
            self.df_comisiones.to_sql('commissions', db_connection, if_exists='replace', index=False)
            self.df_descuentos.to_sql('discounts', db_connection, if_exists='replace', index=False)
            
            # Ejecutar cálculo de comisiones
            print("Ejecutando cálculo de comisiones...")
            df_calculo_comisiones = self.data_loader.load_sql('cc.sql', self.parametros)
            
            return df_calculo_comisiones
        
        except Exception as e:
            print(f"Error al calcular comisiones: {e}")
            raise

    def save_results(self, df_calculo_comisiones):
        """Guarda los resultados en un archivo Excel y en una carpeta de resultados."""
        try:
            print("Guardando resultados...")
            output_dir = f'{self.directorio}/result'
            if not os.path.isdir(output_dir):
                os.mkdir(output_dir)
            
            file_path = f'{output_dir}/Calculo_de_Comisiones.xlsx'
            df_calculo_comisiones.to_excel(file_path, index=False)
            formatear_resultados(file_path)
            return file_path
        except Exception as e:
            print(f"Error al guardar los resultados: {e}")
            raise

    def send_results(self, df_calculo_comisiones):
        """Envía los resultados por correo electrónico con los servidores de Outlook."""
        try:
            print("Preparando y enviando el correo...")  
            body = (  
                f"Estimado/a,<br><br>"  
                f"Adjuntamos la cuenta de cobro correspondiente al período desde {self.parametros['date_init']} hasta {self.parametros['date_end']}.<br><br>"  
                f"A continuación, encontrará un resumen de las comisiones calculadas:<br>{df_calculo_comisiones.to_html(index=False)}<br><br>"  
                f"Saludos cordiales."  
            )  
            self.email_sender.send_email(
                self.parametros['mail_to'],  
                "Resultado de Comisiones",  
                body
            )
        except Exception as e:
            print(e)
            raise

    def run(self):
        """Ejecuta el flujo completo de cargue de datos, cálculo de comisiones y envío de resultados."""
        self.load_data()
        df_calculo_comisiones = self.calculate_commissions()
        self.save_results(df_calculo_comisiones)
        self.send_results(df_calculo_comisiones)