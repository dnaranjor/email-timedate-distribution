import os
import email
from email import policy
from email.parser import BytesParser
import pandas as pd
from collections import defaultdict
from datetime import datetime

# Definir la carpeta que contiene los correos electrónicos
carpeta_correos = r"D:\Users\dnaranjor\OneDrive\Desktop\tmp\emailBKP\input\bandeja"

# Función para leer y analizar cada archivo de correo electrónico
def analizar_correo(archivo):
    with open(archivo, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    
    asunto = msg['subject']
    fecha = msg['date']
    
    if 'Vendiste' in asunto:
        # Convertir la fecha a un objeto datetime
        fecha_dt = datetime.strptime(fecha, '%a, %d %b %Y %H:%M:%S %z')
        return fecha_dt
    return None

# Leer cada archivo en la carpeta y extraer la información necesaria
fechas = []

for archivo in os.listdir(carpeta_correos):
    if archivo.endswith('.eml'):
        ruta_archivo = os.path.join(carpeta_correos, archivo)
        fecha_dt = analizar_correo(ruta_archivo)
        if fecha_dt:
            fechas.append(fecha_dt)

# Crear un DataFrame de pandas para analizar la distribución de fechas y horas
datos = {
    'fecha': fechas,
    'día_de_la_semana': [fecha.strftime('%A') for fecha in fechas],
    'hora': [fecha.strftime('%H') for fecha in fechas]
}

df = pd.DataFrame(datos)

# Generar la tabla de distribución de fechas y horas
tabla_distribucion = df.groupby(['día_de_la_semana', 'hora']).size().unstack(fill_value=0)

# Mostrar la tabla de distribución
print(tabla_distribucion)

# Guardar la tabla de distribución en un archivo CSV
tabla_distribucion.to_csv('distribucion_correos.csv')

