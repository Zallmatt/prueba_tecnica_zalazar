import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class LoadPage:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def open_url_in_new_tab(self, url):
        # Abrir una nueva pestaña y cargar la URL
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(url)
        
    def wait_for_element(self, locator):
        return WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(locator))

    def scroll_down(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  # Esperar 5 segundos para que se cargue más contenido
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:  # Si la altura no cambia, terminamos
                break
            last_height = new_height
            print(f"Scrolled to: {new_height}px")

    def get_hrefs(self, filter_type, existing_hrefs):
        # Esperar a que la página cargue completamente antes de hacer scroll
        self.wait_for_element((By.CLASS_NAME, 'itemContainer-0-2-226'))

        # Realizar el scroll hacia abajo automáticamente hasta el final de la página
        self.scroll_down()

        # Buscar todos los elementos <li> con la clase específica
        items = self.driver.find_elements(By.CLASS_NAME, 'itemContainer-0-2-226')
        
        # Usar un conjunto para almacenar los enlaces únicos
        hrefs = set()
        
        for item in items:
            try:
                link_element = item.find_element(By.TAG_NAME, 'a')
                href = link_element.get_attribute('href')
                
                # Filtrar solo los enlaces que contienen el tipo especificado (movies o series) y que no están en existing_hrefs
                if link_element.is_displayed() and filter_type in href and href not in existing_hrefs:
                    hrefs.add(href)
                    
            except Exception as e:
                print(f"Error al obtener el enlace: {e}")
                continue

        # Verificación del número de enlaces
        print(f"Total de enlaces únicos encontrados para {filter_type}: {len(hrefs)}")

        return list(hrefs)

    def process_urls(self, urls, filter_type, existing_hrefs):
        all_hrefs = set()
        for url in urls:
            self.open_url_in_new_tab(url)
            hrefs = self.get_hrefs(filter_type, existing_hrefs)
            all_hrefs.update(hrefs)
            # Cerrar la pestaña actual y volver a la original
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        return list(all_hrefs)


class LoadPage:
    def load_existing_hrefs(self, csv_filename):
        # Verificar si el archivo existe y no está vacío
        if os.path.exists(csv_filename) and os.path.getsize(csv_filename) > 0:
            df = pd.read_csv(csv_filename)
            # Suponiendo que la columna de enlaces se llama "Link"
            if 'Link' in df.columns:
                return df['Link'].tolist()
            else:
                print(f"No se encontró la columna 'Link' en {csv_filename}.")
                return []
        else:
            print(f"Archivo {csv_filename} no encontrado o está vacío.")
            return []

    def close(self):
        self.driver.quit()
