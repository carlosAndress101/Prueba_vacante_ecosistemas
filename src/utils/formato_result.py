import xlwings as xw

# Ruta del archivo Excel existente
file_path = "ruta_de_tu_archivo.xlsx"  # Cambia esto por la ruta de tu archivo

def formatear_resultados(file_path):
    try:
        App = xw.App(visible=False)
        wb = xw.Book(file_path)
        sheet = wb.sheets[0]  # Asume que la tabla está en la primera hoja

        # Detectar automáticamente el rango de la tabla (desde A1 hasta donde haya datos)
        last_row = sheet.range('A1').end('down').row
        last_col = sheet.range('A1').end('right').column
        table_range = sheet.range((1, 1), (last_row, last_col))

        # Detectar el rango del encabezado
        header_range = sheet.range((1, 1), (1, last_col))

        # Aplicar formato al encabezado
        header_range.color = (0, 112, 192)  # Fondo azul
        header_range.api.Font.Color = 0xFFFFFF  # Letras blancas
        header_range.api.Font.Bold = True  # Negrita
        
        sheet.autofit()


        # Agregar bordes a toda la tabla
        for border_id in range(7, 13):  # IDs de bordes
            table_range.api.Borders(border_id).LineStyle = 1  # Línea continua
            table_range.api.Borders(border_id).Weight = 2  # Grueso medio

        # Guardar los cambios
        wb.save()
        App.quit()
    except Exception as e:
        print(f"Error al formatear los resultados: {e}")
        raise