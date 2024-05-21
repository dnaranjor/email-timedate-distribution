import os
import re
from datetime import datetime
import pandas as pd

# Define the folder that contains the emails
carpeta_correos = r"D:\Users\dnaranjor\OneDrive\Desktop\tmp\emailBKP\input\bandeja"

# Function to read and analyze each email file
def analizar_correo(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    subject = None
    date = None

    for line in lines:
        if line.lower().startswith('subject:'):
            subject = line[len('Subject:'):].strip()
        if line.lower().startswith('date:'):
            date = line[len('Date:'):].strip()
        if subject and date:
            break

    if subject and 'Vendiste' in subject:
        # Convert the date to a datetime object
        try:
            fecha_dt = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z')
            return fecha_dt
        except ValueError as e:
            print(f"Error parsing date {date} in file {archivo}: {e}")
            return None
    return None

# Read each file in the folder and extract the necessary information
fechas = []

for archivo in os.listdir(carpeta_correos):
    if archivo.endswith('.eml'):
        ruta_archivo = os.path.join(carpeta_correos, archivo)
        fecha_dt = analizar_correo(ruta_archivo)
        if fecha_dt:
            fechas.append(fecha_dt)

# Create a pandas DataFrame to analyze the distribution of dates and times
datos = {
    'fecha': fechas,
    'día_de_la_semana': [fecha.strftime('%A') for fecha in fechas],
    'hora': [fecha.strftime('%H') for fecha in fechas]
}

df = pd.DataFrame(datos)

# Generate the distribution table of dates and times
tabla_distribucion = df.groupby(['día_de_la_semana', 'hora']).size().unstack(fill_value=0)

# Display the distribution table
print(tabla_distribucion)

# Save the distribution table to a CSV file
tabla_distribucion.to_csv('distribucion_correos.csv')
