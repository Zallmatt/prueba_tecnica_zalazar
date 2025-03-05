from read_href_on_demand import LoadPage
from read_data import read_data
from read_canales_live_tv import ChannelHrefExtractor
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException
import os


def process_series():
    urls_series = [
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/5f908026a44d9c00081fd41d", #Series para Maratonear
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/625db92c5c4b590007b808c6", #Dramas Coreanos
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/63dd2358a8b22700082367ff", #Series Checas
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941e09db549e0007ef2dc9", #Series Acción
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941dfa8ab0970007f41c59", #Series Sci-Fi
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941de9e03c74000701ed4f", #Series Suspenso
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941dc7fd0bc30007db1b6d", #Series Romance
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/5e2f061eeb7c04000967bf70", #Series Drama
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/5e45bbf395fb000009945cf0", #Series Comedia
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/62473ee1a8099000076c0783", #Series Españolas
        "https://pluto.tv/latam/on-demand/619043246d03190008131b89/6245c1e23ca9b400078727bc"  #Series Latinas
    ]
    all_data = []
    page_loader = LoadPage()
    existing_hrefs = page_loader.load_existing_hrefs('informacion_pluto_series.csv')  #Leer los enlaces ya cargados
    data_loader = None  

    try:
        #Procesar las URLs de las categorías y obtener los hrefs de las series
        hrefs = page_loader.process_urls(urls_series, 'series', existing_hrefs)

        data_loader = read_data()
        page_loader.close()

        total_hrefs = len(hrefs)
        print(f"Total de URLs de series a procesar: {total_hrefs}")

        #Itera sobre cada href y extrae los detalles
        for index, href in enumerate(hrefs, start=1):
            print(f"Procesando URL {index} de {total_hrefs}: {href}")
            try:
                episodes_data = data_loader.extract_details_series(href)
                all_data.extend(episodes_data)  
            except TimeoutException:
                print(f"Error de tiempo de espera al procesar la URL: {href}. Continuando con la siguiente URL.")
            except Exception as e:
                print(f"Error al procesar la URL {href}: {e}. Continuando con la siguiente URL.")

            #Guardar los resultados cada 10 iteraciones o al final del procesamiento
            if index % 10 == 0 or index == total_hrefs:
                df = pd.DataFrame(all_data, columns=[
                    "Titulo", 
                    "Rating", 
                    "Genero", 
                    "Descripcion", 
                    "Temporadas", 
                    "Link", 
                    "Titulo Capitulo", 
                    "Episodio", 
                    "Duracion", 
                    "Descripcion Capitulo", 
                    "Link Capitulo"
                ])
                if not df.empty:
                    file_exists = os.path.isfile('informacion_pluto_series.csv')
                    df.to_csv('informacion_pluto_series.csv', mode='a', header=not file_exists, index=False)
                    all_data.clear()  
                print(f"Progreso guardado: {index} de {total_hrefs} URLs procesadas")
    finally:
        if data_loader:  
            data_loader.close()


def process_channels():
    all_data = []
    extractor = ChannelHrefExtractor()
    existing_hrefs = LoadPage().load_existing_hrefs('informacion_pluto_canales.csv')  #Leer los enlaces ya cargados
    data_loader = None 

    try:
        extractor.open_url('https://pluto.tv/latam/live-tv/63eb9255c111bc0008fe6ec4') 
        hrefs = extractor.click_and_extract()

        hrefs = [href for href in hrefs if href not in existing_hrefs]

        data_loader = read_data()

        total_hrefs = len(hrefs)
        print(f"Total de URLs de canales a procesar: {total_hrefs}")

        for index, href in enumerate(hrefs, start=1):
            print(f"Procesando URL {index} de {total_hrefs}: {href}")
            try:
                data = data_loader.extract_details_channels(href)
                all_data.append(data)  
            except TimeoutException:
                print(f"Error de tiempo de espera al procesar la URL: {href}. Continuando con la siguiente URL.")
            except Exception as e:
                print(f"Error al procesar la URL {href}: {e}. Continuando con la siguiente URL.")

            #Guardar los resultados cada 10 iteraciones o al final del procesamiento
            if index % 10 == 0 or index == total_hrefs:
                df = pd.DataFrame(all_data, columns=[
                    "Titulo",
                    "Descripcion",
                    "Link"
                ])
                if not df.empty:
                    file_exists = os.path.isfile('informacion_pluto_canales.csv')
                    df.to_csv('informacion_pluto_canales.csv', mode='a', header=not file_exists, index=False)
                    all_data.clear()  
                print(f"Progreso guardado: {index} de {total_hrefs} URLs procesadas")
    finally:
        extractor.close()
        if data_loader:  
            data_loader.close()

if __name__ == "__main__":
    start_time = time.time() 

    try:
        print("Procesando películas...")
        process_movies()

        print("Procesando series...")
        process_series()

        print("Procesando canales...")
        process_channels()

    except TimeoutException:
        print("Error de tiempo de espera al obtener los hrefs. Verifica si la página ha cargado correctamente.")
    
    finally:
        end_time = time.time() 
        elapsed_time = end_time - start_time  
        print(f"Tiempo total de ejecución: {elapsed_time:.2f} segundos")
