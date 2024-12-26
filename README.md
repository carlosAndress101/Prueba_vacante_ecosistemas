# Proyecto de Automatización de Cálculo de Comisiones
Este proyecto tiene como objetivo la automatización del cálculo de comisiones para BATSEJ OPEN FINANCE S.A., utilizando Python, SQLite y Outlook para la generación de reportes. La solución permite calcular las comisiones mensuales de cinco empresas de acuerdo con sus contratos específicos, aplicar descuentos y enviar un correo con los resultados. Los resultados también se almacenan en un archivo Excel para su posterior análisis.
## Tabla de Contenidos
* Requisitos
* Estructura del Proyecto
* Descripción de las Clases
* Instalación y Uso
* Ejemplo de Ejecución

## Requisitos
* Python
* SQLite
* Bibliotecas de Python:
* pandas
* openpyxl
* smtplib
* msal
* os

## Estructura del Proyecto
El proyecto está organizado en la siguiente estructura de directorios:
```bash

src/
│
├── Class/                    # Clases principales (Comisiones, DataLoader, EmailSendOutlook)
│   ├── comisiones.py
│   ├── data.py
│   └── email.py
|
├── db/                       # Base de datos SQLite
│   └── database.sqlite
|
├── remote_sql_call/          # Archivos SQL para consultas personalizadas
│   ├── count_call_api.sql
│   └── cc.sql
│
├── result/                 # Carpeta donde se guardan los resultados
|
├── utils/                  # Archivos de guia o funciones adicionales.
│   └── Prueba de conocimiento técnico para automatización.pdf
│
└── main.py                   # Script principal para ejecutar la automatización

```

## Descripción de las Clases
`Comisiones`
La clase Comisiones es la clase principal encargada de:

1. Cargar los datos: Obtiene las tablas commissions y discounts desde la base de datos SQLite.
2. Calcular las comisiones: Realiza el cálculo de las comisiones de acuerdo con los contratos de cada empresa, considerando tanto comisiones fijas como variables, y aplicando descuentos y el IVA del 19%.
3. Guardar los resultados: Almacena los resultados de las comisiones en un archivo Excel en la carpeta /result.
4. Enviar los resultados por correo electrónico: Utiliza el servicio de Outlook para enviar los resultados de las comisiones al correo electrónico de contacto.
   
`DataLoader`
La clase DataLoader se encarga de:

1. Conectar a la base de datos SQLite.
2. Cargar tablas como DataFrames de pandas: Extrae las tablas necesarias desde la base de datos.
3. Ejecutar consultas SQL personalizadas: Lee archivos SQL y ejecuta las consultas necesarias para calcular las estadísticas.

`EmailSendOutlook`
La clase EmailSendOutlook se encarga de:

1. Autenticar el usuario en Outlook mediante OAuth2.
2. Enviar correos electrónicos con los resultados de las comisiones y el archivo Excel adjunto.

## Instalación y Uso
### 1. Clonar el repositorio:
```
git clone https://github.com/carlosAndress101/Prueba_vacante_ecosistemas.git
cd Prueba_vacante_ecosistemas
```
### 2. Configuración del entorno
Después de clonar el proyecto, abre la carpeta donde se encuentra. En la consola, navega hasta el directorio del proyecto y ejecuta el archivo setup.bat con el siguiente comando:
```
./setup.bat
```
Alternativamente, puedes ejecutar el archivo `.bat` simplemente haciendo doble clic sobre él desde el explorador de archivos.
El archivo `.bat` nos permite ahorrar tiempo al crear automáticamente un entorno virtual (`venv`) e instalar las dependencias que se encuentran en el archivo `requirements.txt`. Si lo ejecutas desde la consola de Visual Studio Code, también evitarás la necesidad de activar manualmente el entorno virtual, ya que esto se realizará de manera automática.

## Parámetros Necesarios
### 1. Parámetros de Configuración General
Estos parámetros son necesarios para la inicialización y configuración del codigo, definidos en la tabla parameters en la base de datos:

`mail_to`: Dirección de correo electrónico a la que se enviarán las notificaciones.
Ejemplo: `example@gmail.com`

`subject`: Asunto del correo enviado.
Ejemplo: `"Cuenta de cobro comisiones"`

`date_init`: Fecha de inicio del período a evaluar, en formato YYYYMMDDHHMMSS.
Ejemplo: `20240701000000`

`date_end`: Fecha de fin del período a evaluar, en formato YYYYMMDDHHMMSS.
Ejemplo: `20240831235959`

`trade_status`: Estado del comercio para filtrar datos relevantes (Active, Inactive, etc.).
Ejemplo: `Active`

`client_id`: Identificador único del cliente o sistema asociado.
Ejemplo: `OluLkp5fenU2xbNHZBdKDy8mP6Mw4grQad`

`tenant_id`: Identificador único del tenant (entidad separada dentro del sistema).
Ejemplo: `OluLkp5fsdfU4xbNHZBdKDy8mP6MSd`

`password`: Contraseña asociada a la autenticación del sistema.
Ejemplo: `12345678`

