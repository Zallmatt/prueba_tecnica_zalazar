import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ChannelHrefExtractor:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def open_url(self, url):
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(2)  

    def wait_for_element(self, locator):
        return WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(locator))

    def click_expand_guide(self):
        try:
            #Esperar a que aparezca el boton de 'Guía de Canales de TV'
            expand_button = self.wait_for_element((By.XPATH, "//span[contains(text(),'Guía de Canales de TV')]"))
            expand_button.click()
            print("Botón de 'Guía de Canales de TV' clickeado.")
            time.sleep(3) 
        except Exception as e:
            print(f"No se pudo hacer clic en 'Guía de Canales de TV': {e}")

    def scroll_down_category_list(self):
        try:
            category_container = self.wait_for_element((By.CLASS_NAME, 'scrollContainer-0-2-238'))
            #Desplazarse hacia abajo en el contenedor de categorías
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", category_container)
            time.sleep(2)
            print("Se realizó el scroll en la lista de categorías.")
        except Exception as e:
            print(f"Error al intentar hacer scroll en la lista de categorías: {e}")

    def click_and_extract(self):
        self.wait_for_element((By.CLASS_NAME, 'scrollContainer-0-2-238'))
        categories = self.driver.find_elements(By.CLASS_NAME, 'item-0-2-241')
        all_hrefs = []
        unique_parts = set()
        for i, category in enumerate(categories):
            try:
                print(f"Haciendo clic en la categoría {i + 1} de {len(categories)}")
                category.click()
                time.sleep(3)
                if i == 2:
                    self.click_expand_guide()
                hrefs = self.get_channel_hrefs()
                for href in hrefs:
                    unique_part = href.split('/details')[0]
                    if unique_part not in unique_parts:
                        unique_parts.add(unique_part)
                        all_hrefs.append(href)

                #Desplazar hacia abajo para no perder la vision por pantalla de las categorias
                if i == 5:
                    self.scroll_down_category_list()
                                    
            except Exception as e:
                print(f"Error al intentar extraer hrefs en una categoría: {e}")

        print(f"Total de enlaces de canales únicos encontrados: {len(all_hrefs)}")
        return all_hrefs

    def get_channel_hrefs(self):
        self.wait_for_element((By.CLASS_NAME, 'ChannelInfo-Link'))
        channels = self.driver.find_elements(By.CLASS_NAME, 'ChannelInfo-Link')
        hrefs = [channel.get_attribute('href') for channel in channels]
        print(f"Enlaces encontrados en esta categoría: {len(hrefs)}")
        return hrefs

    def close(self):
        self.driver.quit()
