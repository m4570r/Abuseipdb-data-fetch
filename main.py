import os
import requests
import json
import csv

# Leer la configuración desde el archivo config.json
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

# Obtener la ruta del archivo CSV desde la configuración
file_path = config_data.get('csv_path')

# Obtener la API_KEY y la URL de AbuseIPDB desde la configuración
api_key = config_data.get('api_key')
abuseipdb_url = config_data.get('abuseipdb_url')

# Verificar si el archivo CSV existe en la ruta especificada
if not os.path.exists(file_path):
    # Si el archivo no existe, crear uno con las columnas especificadas y una fila de valores predeterminados
    csv_columns = [
        'ipAddress', 'isPublic', 'isTor', 'ipVersion', 'isWhitelisted',
        'abuseConfidenceScore', 'countryCode', 'usageType', 'isp',
        'domain', 'hostnames', 'totalReports', 'numDistinctUsers',
        'lastReportedAt', 'abuseIPDBLink', 'thisIPNotReported'
    ]
    with open(file_path, 'w', newline='') as filecsv:
        writer = csv.DictWriter(filecsv, fieldnames=csv_columns, delimiter=';')
        writer.writeheader()

# Leer las direcciones IP desde el archivo de texto
with open('ip_list.txt', 'r') as ip_file:
    ip_addresses = ip_file.read().split(',')

# Crear un conjunto de IPs existentes para evitar duplicados
existing_ips = set(ip_addresses)

# Iterar a través de las direcciones IP y agregar los datos al CSV
csv_columns = [
    'ipAddress', 'isPublic', 'isTor', 'ipVersion', 'isWhitelisted',
    'abuseConfidenceScore', 'countryCode', 'usageType', 'isp',
    'domain', 'hostnames', 'totalReports', 'numDistinctUsers',
    'lastReportedAt', 'abuseIPDBLink', 'thisIPNotReported'
]

with open(file_path, 'a', newline='') as filecsv:
    writer = csv.DictWriter(filecsv, fieldnames=csv_columns, delimiter=';')

    for ip in existing_ips:
        # Realizar una solicitud HTTP a AbuseIPDB para obtener datos relacionados con la IP
        parameters = {
            'ipAddress': ip,
            'maxAgeInDays': '90'
        }
        headers = {
            'Accept': 'application/json',
            'Key': api_key
        }

        response = requests.get(url=abuseipdb_url, headers=headers, params=parameters)

        # Verificar si la respuesta es válida antes de intentar analizarla como JSON
        if response.status_code == 200:
            try:
                ip_data = response.json().get('data', {})  # Obtener el diccionario 'data' del JSON
                
                # Generar el enlace a AbuseIPDB con la IP actual
                ip_data['abuseIPDBLink'] = f'https://www.abuseipdb.com/check/{ip}'
                
                # Agregar el campo "thisIPNotReported" al diccionario
                ip_data['thisIPNotReported'] = "This IP address has not been reported" if ip_data['totalReports'] == 0 else "This IP address has been reported"
                
                # Escribir la fila en el archivo CSV
                writer.writerow(ip_data)
            except json.JSONDecodeError as e:
                print(f'Error al decodificar JSON: {e}')
        else:
            print(f'Error al realizar la solicitud HTTP para la IP {ip}. Código de estado: {response.status_code}')
