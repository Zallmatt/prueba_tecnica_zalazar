from read_href_on_demand_movies import LoadPage
from read_data_movies import read_data
from read_canales import ChannelHrefExtractor
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException
import os

def process_movies():
    urls_movies = [
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/6245e3e75b72240007129448", 
        # otras URLs
    ]
    all_data = []
    page_loader = LoadPage()
    existing_hrefs = page_loader.load_existing_hrefs('informacion_pluto_movies.csv')  # Cargar los enlaces existentes
    data_loader = None  # Inicializar data_loader en None
    
    try:
        # Procesar las URLs de las categorías y obtener los hrefs de las películas
        hrefs = page_loader.process_urls(urls_movies, 'movies', existing_hrefs)

        # Inicializa la clase para extraer los detalles de cada href
        data_loader = read_data()
        page_loader.close()

        total_hrefs = len(hrefs)
        print(f"Total de URLs de películas a procesar: {total_hrefs}")

        # Itera sobre cada href y extrae los detalles
        for index, href in enumerate(hrefs, start=1):
            print(f"Procesando URL {index} de {total_hrefs}: {href}")
            try:
                data = data_loader.extract_details_movies(href)
                all_data.append(data)  # Agrega los detalles a la lista
            except TimeoutException:
                print(f"Error de tiempo de espera al procesar la URL: {href}. Continuando con la siguiente URL.")
            except Exception as e:
                print(f"Error al procesar la URL {href}: {e}. Continuando con la siguiente URL.")

        # Crear un DataFrame con los datos obtenidos
        df = pd.DataFrame(all_data)

        if not df.empty:
            file_exists = os.path.isfile('informacion_pluto_movies.csv')
            df.to_csv('informacion_pluto_movies.csv', mode='a', header=not file_exists, index=False)

        print("Datos de películas guardados en informacion_pluto_movies.csv")
    finally:
        if data_loader:  # Solo cierra data_loader si ha sido inicializado
            data_loader.close()

def process_series():
    urls_series = [
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/5f908026a44d9c00081fd41d",
        # otras URLs
    ]
    all_data = []
    page_loader = LoadPage()
    existing_hrefs = page_loader.load_existing_hrefs('informacion_pluto_series.csv')  # Cargar los enlaces existentes
    data_loader = None  # Inicializar data_loader en None

    try:
        # Procesar las URLs de las categorías y obtener los hrefs de las series
        hrefs = page_loader.process_urls(urls_series, 'series', existing_hrefs)

        # Inicializa la clase para extraer los detalles de cada href
        data_loader = read_data()
        page_loader.close()

        total_hrefs = len(hrefs)
        print(f"Total de URLs de series a procesar: {total_hrefs}")

        # Itera sobre cada href y extrae los detalles
        for index, href in enumerate(hrefs, start=1):
            print(f"Procesando URL {index} de {total_hrefs}: {href}")
            try:
                data = data_loader.extract_details_series(href)
                all_data.append(data)  # Agrega los detalles a la lista
            except TimeoutException:
                print(f"Error de tiempo de espera al procesar la URL: {href}. Continuando con la siguiente URL.")
            except Exception as e:
                print(f"Error al procesar la URL {href}: {e}. Continuando con la siguiente URL.")

        # Crear un DataFrame con los datos obtenidos
        df = pd.DataFrame(all_data)

        if not df.empty:
            file_exists = os.path.isfile('informacion_pluto_series.csv')
            df.to_csv('informacion_pluto_series.csv', mode='a', header=not file_exists, index=False)

        print("Datos de series guardados en informacion_pluto_series.csv")
    finally:
        if data_loader:  # Solo cierra data_loader si ha sido inicializado
            data_loader.close()

def process_channels():
    all_data = []
    extractor = ChannelHrefExtractor()
    existing_hrefs = LoadPage().load_existing_hrefs('informacion_pluto_canales.csv')  # Cargar los enlaces existentes
    data_loader = None  # Inicializar data_loader en None

    try:
        extractor.open_url('https://pluto.tv/latam/live-tv/63eb9255c111bc0008fe6ec4')  # URL de canales en vivo
        hrefs = extractor.click_and_extract()

        # Filtrar hrefs para no procesar los que ya están en el CSV
        hrefs = [href for href in hrefs if href not in existing_hrefs]

        # Inicializa la clase para extraer los detalles de cada href
        data_loader = read_data()

        total_hrefs = len(hrefs)
        print(f"Total de URLs de canales a procesar: {total_hrefs}")

        # Itera sobre cada href y extrae los detalles
        for index, href in enumerate(hrefs, start=1):
            print(f"Procesando URL {index} de {total_hrefs}: {href}")
            try:
                data = data_loader.extract_details_channels(href)
                all_data.append(data)  # Agrega los detalles a la lista
            except TimeoutException:
                print(f"Error de tiempo de espera al procesar la URL: {href}. Continuando con la siguiente URL.")
            except Exception as e:
                print(f"Error al procesar la URL {href}: {e}. Continuando con la siguiente URL.")

        # Crear un DataFrame con los datos obtenidos
        df = pd.DataFrame(all_data)

        if not df.empty:
            file_exists = os.path.isfile('informacion_pluto_canales.csv')
            df.to_csv('informacion_pluto_canales.csv', mode='a', header=not file_exists, index=False)

        print("Datos de canales guardados en informacion_pluto_canales.csv")
    finally:
        extractor.close()
        if data_loader:  # Solo cierra data_loader si ha sido inicializado
            data_loader.close()

if __name__ == "__main__":
    start_time = time.time()  # Anotar el tiempo de inicio

    try:
        print("Procesando películas...")
        #process_movies()

        print("Procesando series...")
        #process_series()

        print("Procesando canales...")
        process_channels()

    except TimeoutException:
        print("Error de tiempo de espera al obtener los hrefs. Verifica si la página ha cargado correctamente.")
    
    finally:
        end_time = time.time()  # Anotar el tiempo de finalización
        elapsed_time = end_time - start_time  # Calcular el tiempo total de ejecución
        print(f"Tiempo total de ejecución: {elapsed_time:.2f} segundos")
