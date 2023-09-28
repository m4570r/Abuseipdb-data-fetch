## Descripción

El script realiza las siguientes acciones:

- Lee la configuración desde un archivo JSON llamado 'config.json', que contiene la información de la ruta del archivo CSV, la clave de la API y la URL de AbuseIPDB.
- Comprueba si el archivo CSV especificado en la configuración existe. Si no existe, crea un archivo CSV con columnas específicas.
- Lee las direcciones IP desde un archivo de texto llamado 'ip_list.txt'.
- Crea un conjunto de direcciones IP existentes para evitar duplicados.
- Itera a través de las direcciones IP y realiza solicitudes HTTP a AbuseIPDB para obtener datos relacionados con cada IP.
- Procesa las respuestas JSON recibidas y escribe los datos en el archivo CSV.

## Detalles técnicos

- El script utiliza las bibliotecas estándar de Python, como `os`, `requests`, `json`, y `csv`.
- Lee la configuración de un archivo JSON (`config.json`) que debe estar en el mismo directorio que el script.
- Utiliza una clave de API (obtenida de la configuración) para autenticarse en AbuseIPDB.
- Las direcciones IP se leen desde un archivo de texto (`ip_list.txt`) y se almacenan en un conjunto (`existing_ips`) para evitar duplicados.
- Realiza solicitudes HTTP GET a AbuseIPDB para obtener datos relacionados con cada IP en el conjunto.
- Verifica el código de estado de la respuesta HTTP. Si es 200 (OK), procesa la respuesta JSON y agrega los datos relevantes al archivo CSV.
- El archivo CSV se crea si no existe y contiene las siguientes columnas: 'ipAddress', 'isPublic', 'isTor', 'ipVersion', 'isWhitelisted', 'abuseConfidenceScore', 'countryCode', 'usageType', 'isp', 'domain', 'hostnames', 'totalReports', 'numDistinctUsers', 'lastReportedAt', 'abuseIPDBLink', 'thisIPNotReported'.
- El campo 'abuseIPDBLink' contiene un enlace a la página de AbuseIPDB para la IP correspondiente.
- El campo 'thisIPNotReported' indica si la IP ha sido reportada o no.

En resumen, este script se utiliza para recopilar información sobre direcciones IP desde AbuseIPDB y almacenarla en un archivo CSV para su posterior análisis o seguimiento de abusos de IP. Asegúrate de proporcionar la configuración necesaria en el archivo 'config.json' y las direcciones IP en 'ip_list.txt' antes de ejecutar el script.
