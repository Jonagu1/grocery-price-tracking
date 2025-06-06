from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import csv

# Configurar el navegador
options = webdriver.ChromeOptions()
arguments = ["--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--disable-renderer-backgrounding", "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows", "--disable-client-side-phishing-detection", "--disable-crash-reporter", "--disable-oopr-debug-crash-dump",
            "--no-crash-upload", "--disable-gpu", "--disable-extensions", "--disable-low-res-tiling", "--log-level=3", "--silent"]
for argument in arguments: options.add_argument(argument)
driver = webdriver.Chrome(options=options)

# Archivo donde se guardarán los resultados
actual = datetime.now().strftime("%d-%m-%Y")
archivo_salida = f"results/{actual}.csv"

with open(archivo_salida, "w", encoding="utf-8") as archivo:
    with open("search_list.txt", "r", encoding="utf-8") as lista:
        writer = csv.writer(archivo)
        writer.writerow(["search","found", "price", "pre_discount"])
        for linea in lista:
            producto = linea.strip()
            if producto:
                url = f"https://www.jumbo.cl/busqueda?ft={producto}"
                print(f"\n Buscando: {producto}")
                driver.get(url)

                try:
                    # Esperar hasta que aparezcan contenedores de productos
                    
                    contenedores = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"product-card")))
                    if not contenedores:
                        raise Exception("No se encontraron contenedores")

                    for contenedor in contenedores:
                        marca_elemento = contenedor.find_element(By.CSS_SELECTOR, ".product-card .product-card-brand").text
                        nombre_elemento = contenedor.find_element(By.CLASS_NAME, "product-card-name")
                        nombre_producto = f"{marca_elemento} {nombre_elemento.text}"
                        precio_elemento = contenedor.find_element(By.CLASS_NAME, "prices-main-price").text
                        precio_elemento = precio_elemento.replace("$", "")
                        precio_elemento = precio_elemento.replace(".", "")
                        try:
                            old_price = contenedor.find_element(By.CLASS_NAME, "prices-old-price").text
                            old_price=old_price.replace(".", "")
                            old_price=old_price.replace("$","")
                        except:
                            old_price = precio_elemento
                        print(f" {nombre_producto} |  {precio_elemento}")
                        
                        writer.writerow([producto,nombre_producto, precio_elemento,old_price])

                except Exception as e:
                    print(f" No se encontró información para {producto}")
                time.sleep(2)

driver.quit()
print(f"\n :D Datos guardados en '{archivo_salida}'")
