import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoadPage:
    def __init__(self):
        self.driver = webdriver.Chrome()
        #self.driver.get('https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/6245e3e75b72240007129448')

    def scroll_down(self):
        # Scroll hacia abajo en incrementos
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollBy(0, 1000);")  # Desplazarse hacia abajo 1000 píxeles
            time.sleep(2)  # Esperar un poco para que la página cargue
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:  # Si la altura no cambia, terminamos
                break
            last_height = new_height
            print(f"Scrolled to: {new_height}px")

    def wait_for_element(self, locator):
        return WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(locator))

    def get_hrefs(self):
        # Primero, hacer scroll hacia abajo para cargar todos los elementos
        self.scroll_down()

        # Ahora buscar todos los elementos con la clase 'itemContainer'
        items = self.driver.find_elements(By.CLASS_NAME, 'itemContainer')
        
        # Usar un conjunto para almacenar los enlaces únicos
        hrefs = set()
        
        for item in items:
            try:
                link_element = item.find_element(By.TAG_NAME, 'a')
                href = link_element.get_attribute('href')
                
                # Solo agregar si no está en el conjunto
                if link_element.is_displayed() and href not in hrefs:
                    hrefs.add(href)
                    
            except Exception as e:
                print(f"Error al obtener el enlace: {e}")
                continue

        # Verificación del número de enlaces
        print(f"Total de enlaces únicos encontrados: {len(hrefs)}")

        return list(hrefs)

    def extract_details(self, url):
        self.driver.get(url)
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

        print(f"Title: {title}")
        print(f"Rating: {rating}")
        print(f"Genre: {genre}")
        print(f"Synopsis: {synopsis}")
        print(f"Link: {url}")
        print(f"Duration: {duration}")
        print('-' * 40)

        return {
            "Title": title,
            "Rating": rating,
            "Genre": genre,
            "Synopsis": synopsis,
            "Link": url,
            "Duration": duration
        }

    def close(self):
        self.driver.quit()

# Uso de la clase
if __name__ == "__main__":
    page_loader = LoadPage()
    details = page_loader.extract_details('https://pluto.tv/latam/on-demand/movies/649c886c12c80e0013cd187e/details?lang=en')
    #try:
        #hrefs = page_loader.get_hrefs()
        #print(hrefs)
        
        # Extraer detalles para cada href
        #for href in hrefs:
        #    details = page_loader.extract_details(href)
            # Aquí podrías almacenar o procesar la información como desees
        #    print(details)

    #finally:
        # Asegurarse de cerrar el navegador al finalizar
        #page_loader.close()
