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
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/631a0596822bbc000747c340",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/604a66306fb8e0000718b7d5",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/6144cbd27bdf170007e1ea12",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/6419c584dbdaaa000845cad0",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e2efdab7606430009a60684",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/6245bf61a380fd00075eb902",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e664a3d461ef80007c74a4b",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e2f057012f8f9000947823a",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e664ad54d9608000711bf62",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e98ba08d29fad000774d8f1",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e45b93b0226550009f458f0",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e45b6c57cbf380009c9fd3c",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e45bb571dbf7b000935ab55",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/60cb966907f6370007c0e05e",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e664aac9cbc7000077f8ad9",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5e98badabe135f0007f6fd38",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/60c0cc32c72308000700c61a",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/60cb97ae9f11af0007902c42",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/62473fdd9c333900071c587e",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/5f90b50775cc210007c85400",
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/669eb36efe11e500084757fb"
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

            # Guardar los resultados cada 10 iteraciones
            if index % 10 == 0 or index == total_hrefs:
                df = pd.DataFrame(all_data)
                if not df.empty:
                    file_exists = os.path.isfile('informacion_pluto_movies.csv')
                    df.to_csv('informacion_pluto_movies.csv', mode='a', header=not file_exists, index=False)
                    all_data.clear()  # Limpiar la lista después de guardar para evitar duplicados
                print(f"Progreso guardado: {index} de {total_hrefs} URLs procesadas")

    finally:
        if data_loader:  # Solo cierra data_loader si ha sido inicializado
            data_loader.close()

def process_series():
    urls_series = [
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/5f908026a44d9c00081fd41d",
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/625db92c5c4b590007b808c6",
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/63dd2358a8b22700082367ff",
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941e09db549e0007ef2dc9",
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941dfa8ab0970007f41c59",
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941de9e03c74000701ed4f",
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941dc7fd0bc30007db1b6d",
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/5e2f061eeb7c04000967bf70",
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/5e45bbf395fb000009945cf0",
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/62473ee1a8099000076c0783",
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/6245c1e23ca9b400078727bc"
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
                episodes_data = data_loader.extract_details_series(href)
                all_data.extend(episodes_data)  # Agregar los detalles de los episodios a la lista de datos
            except TimeoutException:
                print(f"Error de tiempo de espera al procesar la URL: {href}. Continuando con la siguiente URL.")
            except Exception as e:
                print(f"Error al procesar la URL {href}: {e}. Continuando con la siguiente URL.")

            # Guardar los resultados cada 10 iteraciones
            if index % 10 == 0  or index == total_hrefs:
                df = pd.DataFrame(all_data)
                if not df.empty:
                    file_exists = os.path.isfile('informacion_pluto_series.csv')
                    df.to_csv('informacion_pluto_series.csv', mode='a', header=not file_exists, index=False)
                    all_data.clear()  # Limpiar la lista después de guardar para evitar duplicados
                print(f"Progreso guardado: {index} de {total_hrefs} URLs procesadas")

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

            # Guardar los resultados cada 10 iteraciones
            if index % 10 == 0 or index == total_hrefs:
                df = pd.DataFrame(all_data)
                if not df.empty:
                    file_exists = os.path.isfile('informacion_pluto_canales.csv')
                    df.to_csv('informacion_pluto_canales.csv', mode='a', header=not file_exists, index=False)
                    all_data.clear()  # Limpiar la lista después de guardar para evitar duplicados
                print(f"Progreso guardado: {index} de {total_hrefs} URLs procesadas")

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
        process_series()

        print("Procesando canales...")
        #process_channels()

    except TimeoutException:
        print("Error de tiempo de espera al obtener los hrefs. Verifica si la página ha cargado correctamente.")
    
    finally:
        end_time = time.time()  # Anotar el tiempo de finalización
        elapsed_time = end_time - start_time  # Calcular el tiempo total de ejecución
        print(f"Tiempo total de ejecución: {elapsed_time:.2f} segundos")
