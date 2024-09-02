from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

class LiveTVExtractor:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def open_url(self, url):
        self.driver.get(url)
        time.sleep(15)  # Espera para que la página cargue completamente

    def extract_live_tv_grid(self):
        programs = []
        grid_items = self.driver.find_elements(By.CLASS_NAME, 'timelineItem-0-2-333')

        for item in grid_items:
            try:
                title_element = item.find_element(By.CLASS_NAME, 'name-item')
                title = title_element.text if title_element else "N/A"

                time_element = item.find_element(By.CLASS_NAME, 'time-0-2-345')
                start_time = time_element.text.split('.')[0] if time_element else "N/A"
                end_time = time_element.text.split('.')[1] if time_element else "N/A"

                link_element = item.find_element(By.TAG_NAME, 'a')
                link = link_element.get_attribute('href') if link_element else "N/A"

                programs.append({
                    "Titulo": title,
                    "Hora de Inicio": start_time,
                    "Hora de Fin": end_time,
                    "Link": link
                })
            except Exception as e:
                print(f"Error al extraer datos de un programa: {e}")
                continue  # Continúa con el siguiente programa si hay un error

        return programs

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    live_tv_url = "https://pluto.tv/latam/live-tv/5dcde437229eff00091b6c30"
    extractor = LiveTVExtractor()

    try:
        extractor.open_url(live_tv_url)
        programs = extractor.extract_live_tv_grid()

        # Crear un DataFrame con los datos obtenidos
        df = pd.DataFrame(programs)
        
        # Guardar el DataFrame en un archivo CSV
        df.to_csv('grilla_live_tv.csv', index=False)

        print("Datos de la grilla de Live TV guardados en grilla_live_tv.csv")
    finally:
        extractor.close()
