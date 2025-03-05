import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
def get_categories():
    url = "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0"
    response = requests.get(url)
    if response.status_code != 200:
        print("Error al obtener la página principal.")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    category_links = []
    
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "/on-demand/618da9791add6600071d68b0/" in href and href not in category_links:
            category_links.append("https://pluto.tv" + href)
    
    print(category_links)

    return category_links

def get_movie_links(category_url):
    response = requests.get(category_url)
    if response.status_code != 200:
        print(f"Error al obtener la categoría: {category_url}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_links = []
    
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "/on-demand/movies/" in href and href not in movie_links:
            movie_links.append("https://pluto.tv" + href + "/details")
    
    print("***************************")
    print("Peliculas")
    print(movie_links)

    return movie_links

def extract_movie_details(movie_url):
    options = Options()
    options.add_argument("--headless")  # Ejecutar en modo sin interfaz gráfica
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(movie_url)
        wait = WebDriverWait(driver, 10)

        # Extraer título
        try:
            title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).text.strip()
        except:
            title = "Desconocido"

        # Extraer rating (probando varias opciones)
        try:
            rating = "Desconocido"
            rating_candidates = driver.find_elements(By.XPATH, "//span[contains(@class, 'rating')] | //li[contains(text(), 'TV-')] | //li[contains(text(), 'PG')] | //li[contains(text(), 'R')] | //li[contains(text(), 'G')] | //li[contains(text(), 'NR')]")
            for candidate in rating_candidates:
                text = candidate.text.strip()
                if text and len(text) <= 5:  # Filtrar ratings como "TV-PG", "PG-13", etc.
                    rating = text
                    break
        except:
            rating = "Desconocido"

        # Extraer descripción
        try:
            description = driver.find_element(By.TAG_NAME, "p").text.strip()
        except:
            description = "Sin descripción"

        # Extraer metadata (Género y Duración)
        try:
            metadata_items = driver.find_element(By.XPATH, "//ul[contains(@class, 'metadata')]").find_elements(By.TAG_NAME, 'li')

            IGNORE_WORDS = {"R", "PG", "PG-13", "G", "NR", "TV-MA", "TV-14", "TV-PG", "TV-G", "TV-Y", "TV-Y7", "", " ", "•"}
            genero = next((item.text.strip() for item in metadata_items if item.text.strip() not in IGNORE_WORDS), "N/A")

            duracion = next((item.text.strip() for item in metadata_items if "min" in item.text), "N/A")
        except:
            genero = "Desconocido"
            duracion = "Desconocido"

        # Enlace de la película
        link = movie_url

        # Imprimir detalles
        print("***************************")
        print("Detalles de la Película")
        print(f"Título: {title}")
        print(f"Rating: {rating}")
        print(f"Género: {genero}")
        print(f"Duración: {duracion}")
        print(f"Descripción: {description}")
        print(f"Enlace: {link}")

        return {
            "Título": title,
            "Rating": rating,
            "Género": genero,
            "Duración": duracion,
            "Descripción": description,
            "Enlace": link
        }

    except Exception as e:
        print(f"Error al procesar la película: {e}")
        return None
    finally:
        driver.quit()

def save_to_csv(all_movies):
    # Verificar si la carpeta 'files' existe, si no, crearla
    folder_path = 'files'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Ruta completa del archivo dentro de la carpeta 'files'
    file_path = os.path.join(folder_path, "pluto_movies.csv")

    # Guardar los datos en el archivo CSV dentro de la carpeta 'files'
    if all_movies:
        df = pd.DataFrame(all_movies)
        file_exists = os.path.isfile(file_path)
        df.to_csv(file_path, mode='a', header=not file_exists, index=False)
        print(f"Datos guardados en {file_path}")
    else:
        print("No se encontraron películas.")

def main():
    categories = get_categories()
    all_movies = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_category = {executor.submit(get_movie_links, category): category for category in categories}
        
        for future in as_completed(future_to_category):
            category = future_to_category[future]
            try:
                movie_links = future.result()
                print(f"Procesando categoría: {category}")
                
                with ThreadPoolExecutor(max_workers=5) as movie_executor:
                    future_to_movie = {movie_executor.submit(extract_movie_details, movie): movie for movie in movie_links}
                    
                    for movie_future in as_completed(future_to_movie):
                        movie_data = movie_future.result()
                        if movie_data:
                            all_movies.append(movie_data)
            except Exception as e:
                print(f"Error al procesar la categoría {category}: {e}")

    # Guardar los datos en CSV
    save_to_csv(all_movies)

if __name__ == "__main__":
    start_time = time.time() 
    main()
    end_time = time.time() 
    elapsed_time = end_time - start_time  
    print(f"Tiempo total de ejecución: {elapsed_time:.2f} segundos")
