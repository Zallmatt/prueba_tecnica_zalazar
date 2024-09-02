import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ChannelHrefExtractor:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def open_url(self, url):
        # Abrir la URL
        self.driver.get(url)
        # Maximizar la ventana
        self.driver.maximize_window()
        time.sleep(2)  # Esperar para asegurar que la página se haya cargado correctamente

    def wait_for_element(self, locator):
        return WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(locator))

    def click_expand_guide(self):
        try:
            # Espera a que el botón "Guía de Canales de TV" sea visible y haz clic en él
            expand_button = self.wait_for_element((By.XPATH, "//span[contains(text(),'Guía de Canales de TV')]"))
            expand_button.click()
            print("Botón de 'Guía de Canales de TV' clickeado.")
            time.sleep(3)  # Esperar para asegurar que la guía se haya expandido correctamente
        except Exception as e:
            print(f"No se pudo hacer clic en 'Guía de Canales de TV': {e}")

    def scroll_down_category_list(self):
        try:
            # Identificar el contenedor de las categorías
            category_container = self.wait_for_element((By.CLASS_NAME, 'scrollContainer-0-2-238'))
            # Desplazarse hacia abajo en el contenedor de categorías
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", category_container)
            time.sleep(2)  # Esperar para asegurarse de que el desplazamiento se haya completado
            print("Se realizó el scroll en la lista de categorías.")
        except Exception as e:
            print(f"Error al intentar hacer scroll en la lista de categorías: {e}")

    def click_and_extract(self):
        # Espera a que las categorías estén visibles
        self.wait_for_element((By.CLASS_NAME, 'scrollContainer-0-2-238'))
        categories = self.driver.find_elements(By.CLASS_NAME, 'item-0-2-241')
        
        all_hrefs = []
        unique_parts = set()
        for i, category in enumerate(categories):
            try:
                print(f"Haciendo clic en la categoría {i + 1} de {len(categories)}")
                category.click()
                time.sleep(3)  # Esperar 5 segundos para que los canales de la categoría carguen

                hrefs = self.get_channel_hrefs()
                for href in hrefs:
                    # Extraer la parte del enlace para comparación
                    unique_part = href.split('/details')[0]  # Toma la parte antes de '/details'
                    if unique_part not in unique_parts:
                        unique_parts.add(unique_part)
                        all_hrefs.append(href)

                # Después de cambiar de categoría la primera vez, hacer clic en "Guía de Canales de TV"
                if i == 5:
                    self.click_expand_guide()
                    self.scroll_down_category_list()
                                    
            except Exception as e:
                print(f"Error al intentar extraer hrefs en una categoría: {e}")

        print(f"Total de enlaces de canales únicos encontrados: {len(all_hrefs)}")
        return all_hrefs

    def get_channel_hrefs(self):
        # Espera a que se cargue la lista de canales
        self.wait_for_element((By.CLASS_NAME, 'ChannelInfo-Link'))

        # Encuentra todos los elementos que tienen el href de los canales
        channels = self.driver.find_elements(By.CLASS_NAME, 'ChannelInfo-Link')
        
        # Extrae los hrefs
        hrefs = [channel.get_attribute('href') for channel in channels]
        
        print(f"Enlaces encontrados en esta categoría: {len(hrefs)}")
        return hrefs

    def close(self):
        self.driver.quit()

# Uso de la clase
if __name__ == "__main__":
    extractor = ChannelHrefExtractor()
    extractor.open_url('https://pluto.tv/latam/live-tv/63eb9255c111bc0008fe6ec4')  # Reemplaza con la URL correspondiente
    hrefs = extractor.click_and_extract()
    print(hrefs)
    extractor.close()
