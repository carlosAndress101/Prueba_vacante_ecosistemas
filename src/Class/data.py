import pandas as pd
import sqlite3
import os

class DataLoader:
    """Clase para cargar datos desde archivos Excel y la base de datos SQLite."""
    
    def __init__(self, directorio):
        self.directorio = directorio
        self.db_path = f'{self.directorio}/db/database.sqlite'
        self.connection = self.get_db_connection()
    
    def get_db_connection(self):
        """Obtiene la conexión a la base de datos SQLite."""
        if os.path.exists(self.db_path):
            return sqlite3.connect(self.db_path)
        else:
            raise FileNotFoundError(f'Base de datos "{self.db_path}" no existe')
    
    def load_table_as_dataframe(self, table_name):
        """Carga una tabla completa desde la base de datos como un DataFrame."""
        query = f"SELECT * FROM {table_name}"
        return pd.read_sql_query(query, self.connection)
    
    def load_parameters(self):
        """Carga los parámetros desde la tabla `paremeter` como un diccionario."""
        query = "SELECT paremeter_name, value FROM paremeter"
        df = pd.read_sql_query(query, self.connection)
        return pd.Series(df['value'].values, index=df['paremeter_name']).to_dict()

    def load_sql(self, sql_file, params):
        """Ejecuta una consulta SQL con parámetros y retorna un DataFrame."""
        with open(f'{self.directorio}/remote_sql_call/{sql_file}') as sql_file:
            sql = sql_file.read()
        return pd.read_sql_query(sql.format(**params), self.get_db_connection())
    
    def load_database(self, sql_file, params):
        """Ejecuta una consulta SQL con parámetros y retorna un DataFrame."""
        with open(f'{self.directorio}/db/{sql_file}') as sql_file:
            sql = sql_file.read()
        return pd.read_sql_query(sql.format(**params), self.get_db_connection())
    
    def close_connection(self):
        """Cierra la conexión a la base de datos."""
        if self.connection:
            self.connection.close()