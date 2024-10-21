
# Importamos las librerías que necesitamos

# Librerías de extracción de datos
# -----------------------------------------------------------------------

# Importaciones:
# Beautifulsoup
from bs4 import BeautifulSoup

# Requests
import requests

# Importar librerías para automatización de navegadores web con Selenium
# -----------------------------------------------------------------------
from selenium import webdriver  # Selenium es una herramienta para automatizar la interacción con navegadores web.
from webdriver_manager.chrome import ChromeDriverManager  # ChromeDriverManager gestiona la instalación del controlador de Chrome.
from selenium.webdriver.common.keys import Keys  # Keys es útil para simular eventos de teclado en Selenium.
from selenium.webdriver.support.ui import Select  # Select se utiliza para interactuar con elementos <select> en páginas web.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException # Excepciones comunes de selenium que nos podemos encontrar 


# Importar librerías para pausar la ejecución
# -----------------------------------------------------------------------
from time import sleep  # Sleep se utiliza para pausar la ejecución del programa por un número de segundos.
import os

import dotenv
from dotenv import load_dotenv

load_dotenv()
rapidapi_token = os.getenv("token")


def sacar_info_h2(url):
        res_url = requests.get(url)

    # Verifica el código de estado
        print(res_url.status_code)

    # Si el código de estado es 200, procesa la respuesta
        if res_url.status_code == 200:
            sopa_actividades = BeautifulSoup(res_url.content, "html.parser")
            lista_actividades = sopa_actividades.findAll("h2")
            activ = []
            for actividad in lista_actividades:
                activ.append(actividad.getText(strip=True))

        else:
            print("Error al acceder a la página")

        return activ

def sacar_info(url, que_buscar):
    

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'es',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.getyourguide.es/'
 }

    res_url = requests.get(url, headers=headers)

    # Verifica el código de estado
    print(res_url.status_code)

    # Si el código de estado es 200, procesa la respuesta
    if res_url.status_code == 200:
        sopa_actividades = BeautifulSoup(res_url.content, "html.parser")
        lista_actividades = sopa_actividades.findAll(que_buscar)
        activ = []
        for actividad in lista_actividades:
            activ.append(actividad.getText(strip=True))

        return(activ)
    else:
        print("Error al acceder a la página")




def vuelos_aeropuertos_franceses(num_adultos):
#top vuelos para una pareja (2 adultos) desde Madrid a París en el penúltimo fin de semana de Noviembre (22-25)
    url = "https://sky-scrapper.p.rapidapi.com/api/v2/flights/searchFlightsComplete"
    
    dict_a_franc = {'PARI': '27539733',
 'CDG': '95565041',
 'ORY': '95565040',
 'BVA': '95566278',
 'LBG': '129053609',
 'MBJ': '99539667',
 'KIN': '99539636',
 'PAS': '104120332'}
#En madrid sólo hay un aeropuerto importante, barajas, pero en París hay hasta 8. Iteraremos por cada uno. Ahora omitimos los niños.
    lista_respuestas_funcion = []
    for key, value in dict_a_franc.items():

        querystring = {"originSkyId":"MAD",
                   "destinationSkyId": key,
                   "originEntityId":"95565077",
                   "destinationEntityId": value,
                   "cabinClass":"economy",
                   "adults":num_adultos,
                   "sortBy":"best",
                   "currency":"EUR",
                   "market":"es-ES",
                   "countryCode":"ES",
                   "limit" : "2",
                   "date" : "2024-11-22",
                   "returnDate": "2024-11-25",
       }

        headers = {
	        "x-rapidapi-key": rapidapi_token,
	        "x-rapidapi-host": "sky-scrapper.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        lista_respuestas_funcion.append(response.json())
        print(response.json())


        respuestas = []
# Obtener respuestas desde "data" solo si la clave "data" existe
    for i in lista_respuestas_funcion:
        if "data" in i:
            respuestas.append(i["data"])
        else:
            print(f"Clave 'data' no encontrada en el elemento: {i}")  # Mensaje de depuración

    precio_vuelof = []
    origen_vuelof = []
    destino_vuelof = []

# Iterar sobre la lista de respuestas
    for i in range(len(respuestas)):  # Ajusta el rango al tamaño de las respuestas
        itineraries = respuestas[i].get('itineraries', [])  # Si no existen itinerarios, regresa lista vacía
        for itinerary in itineraries:
            price_raw = itinerary['price']['raw']  # Precio bruto
            price_formatted = itinerary['price']['formatted']  # Precio formateado
            precio_vuelof.append(price_formatted)
        
            legs = itinerary['legs']
            for leg in legs:
                # Acceder a los aeropuertos de origen y destino
                origin_airport = leg['origin']['name']
                destination_airport = leg['destination']['name']
                origen_vuelof.append(origin_airport)
                destino_vuelof.append(destination_airport)
   
        
        # Crear el diccionario combinando las tres listas
    diccionario_vuelos_funcion = {}

    for origen, destino, precio in zip(origen_vuelof, destino_vuelof, precio_vuelof):
    # Verifica si el aeropuerto de origen ya está en el diccionario
        if origen not in diccionario_vuelos_funcion:
            diccionario_vuelos_funcion[origen] = []  # Si no existe, inicializa con una lista vacía
    
    # Añade el destino y precio como una tupla a la lista del aeropuerto de origen
        diccionario_vuelos_funcion[origen].append((destino, precio))

# Ver el diccionario resultante
    return diccionario_vuelos_funcion