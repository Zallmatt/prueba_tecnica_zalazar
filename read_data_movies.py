import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class read_data:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def wait_for_element(self, locator):
        return WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(locator))
        
    def extract_details_movies(self, url):
        self.driver.get(url)
        time.sleep(10)
        self.wait_for_element((By.CLASS_NAME, 'name-0-2-233'))

        try:
            title = self.driver.find_element(By.CLASS_NAME, 'name-0-2-233').text
        except Exception as e:
            print(f"Error al extraer el título: {e}")
            title = "N/A"

        try:
            synopsis = self.driver.find_element(By.CLASS_NAME, 'description-0-2-236').text
        except Exception as e:
            print(f"Error al extraer la sinopsis: {e}")
            synopsis = "N/A"

        try:
            # Extraer el rating directamente del span con clase "rating"
            rating_element = self.driver.find_element(By.XPATH, "//span[@class='rating']")
            rating = rating_element.text if rating_element else "N/A"

            # Extraer el género y la duración usando los metadatos
            metadata_list = self.driver.find_element(By.XPATH, "//ul[contains(@class, 'metadata')]").find_elements(By.TAG_NAME, 'li')
            
            genre = next((item.text for item in metadata_list if item.text not in ["R", "PG", "PG-13", "G", "NR", "TV-MA", "TV-14", "TV-PG", "TV-G", "TV-Y", "TV-Y7", "", " "]), "N/A")
            duration = next((item.text for item in metadata_list if "min" in item.text), "N/A")
            
        except Exception as e:
            print(f"Error al extraer la duración, género y rating: {e}")
            rating = duration = genre = "N/A"

        print(f"Titulo: {title}")
        print(f"Rating: {rating}")
        print(f"Genero: {genre}")
        print(f"Descripcion: {synopsis}")
        print(f"Link: {url}")
        print(f"Duracion: {duration}")
        print('-' * 40)

        return {
            "Titulo": title,
            "Rating": rating,
            "Genero": genre,
            "Descripcion": synopsis,
            "Link": url,
            "Duracion": duration
        }


    def extract_details_series(self, url):
        self.driver.get(url)
        time.sleep(15)
        self.wait_for_element((By.CLASS_NAME, 'name-0-2-233'))

        try:
            title = self.driver.find_element(By.CLASS_NAME, 'name-0-2-233').text
        except Exception as e:
            print(f"Error al extraer el título: {e}")
            title = "N/A"

        try:
            synopsis = self.driver.find_element(By.CLASS_NAME, 'description-0-2-236').text
        except Exception as e:
            print(f"Error al extraer la sinopsis: {e}")
            synopsis = "N/A"

        try:
            # Extraer el rating directamente del span con clase "rating"
            rating_element = self.driver.find_element(By.XPATH, "//span[@class='rating']")
            rating = rating_element.text if rating_element else "N/A"

            # Extraer el género y la duración usando los metadatos
            metadata_list = self.driver.find_element(By.XPATH, "//ul[contains(@class, 'metadata')]").find_elements(By.TAG_NAME, 'li')
            
            genre = next((item.text for item in metadata_list if item.text not in ["R", "PG", "PG-13", "G", "NR", "TV-MA", "TV-14", "TV-PG", "TV-G", "TV-Y", "TV-Y7", "", " "]), "N/A")
            duration = next((item.text for item in metadata_list if "porada" in item.text), "N/A")
            
        except Exception as e:
            print(f"Error al extraer la duración, género y rating: {e}")
            rating = duration = genre = "N/A"

        print(f"Titulo: {title}")
        print(f"Rating: {rating}")
        print(f"Genero: {genre}")
        print(f"Descripcion: {synopsis}")
        print(f"Link: {url}")
        print(f"Temporadas: {duration}")
        print('-' * 40)

        return {
            "Titulo": title,
            "Rating": rating,
            "Genero": genre,
            "Descripcion": synopsis,
            "Link": url,
            "Duracion": duration
        }

    def extract_details_channels(self, url):
        self.driver.get(url)
        time.sleep(5)  # Esperar a que cargue la página

        # Buscar el título utilizando una clase que contenga "name-0-2-"
        try:
            title = self.driver.find_element(By.CSS_SELECTOR, "[class^='name-0-2-']").text
        except Exception as e:
            print(f"Error al extraer el título: {e}")
            title = "N/A"

        # Buscar la sinopsis utilizando una clase que contenga "description-0-2-"
        try:
            synopsis = self.driver.find_element(By.CSS_SELECTOR, "[class^='description-0-2-']").text
        except Exception as e:
            print(f"Error al extraer la sinopsis: {e}")
            synopsis = "N/A"

        print(f"Titulo: {title}")
        print(f"Descripcion: {synopsis}")
        print(f"Link: {url}")
        print('-' * 40)

        return {
            "Titulo": title,
            "Descripcion": synopsis,
            "Link": url,
        }


    def process_urls(self, urls, ejecutar):
        all_data = []
        for url in urls:
            if ejecutar == "peliculas":
                data = self.extract_details_movies(url)
                all_data.append(data)  # Agregar cada resultado a la lista
            elif ejecutar == "series":
                data = self.extract_details_series(url)
                all_data.append(data)  # Agregar cada resultado a la lista
        return all_data

    def close(self):
        self.driver.quit()
