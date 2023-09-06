import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv



# Acá entro a la página semilla
# -------------------------------------------------------

options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
)

# options.add_argument("--headless")

driver = webdriver.Chrome(options=options)
driver.get("https://inmuebles.nocnok.com/propiedades?stateId=20&countyIds=1065&operation=sale&categories=Habitational&types=House&pageNumber=1&pageSize=21")
driver.maximize_window()

# Espero unos segundos después de que cargue la página
sleep(random.uniform(5.0, 6.0))

# Abro un archivo CSV para escritura
with open('casas_nocnok.csv', mode='w', newline='', encoding='utf-8') as file:
    # Crea un objeto csv.writer
    writer = csv.writer(file)
    
    # Escribo la primera fila con los nombres de las columnas
    writer.writerow(['title', 'seller', 'property_type', 'address', 'price', 'bedrooms', 'bathrooms', 'built_Area', 'land_Area', 'parking', 'description'])

    #  Acá me muevo a las pestañas donde están mis datos y los extraigo
    # --------------------------------------------------------------------
    # Obtengo los botones para pasar entre páginas y los recorro con un for
    botones_de_paginacion = driver.find_elements(By.XPATH, "//div[@class='col-xl-12 col-lg-12 col-md-12 col-sm-12']//ul//li[position() >= 2 and position() < last()]")
    for boton_de_paginacion in botones_de_paginacion:
        try:
            driver.execute_script("arguments[0].scrollIntoView();", boton_de_paginacion)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(boton_de_paginacion))
            sleep(random.uniform(3.0, 6.0))
            boton_de_paginacion.click()
            sleep(random.uniform(3.0, 6.0))

            # Obtengo todos los anuncios de casas y los agrego en una lista para
            # extraer los datos uno a uno
            reviews = driver.find_elements(By.XPATH, "//div[@class='col-xxl-4 col-xl-4 col-lg-4 col-md-6 col-sm-6']")
            for review in reviews:
                try:
                    # Me ubico en la parte en donde está el link para abrir la pesataña del usuario
                    userLink = review.find_element(By.XPATH, ".//div[@class='property-card-grid-wrap-details']/span/a")
                    
                    # Le doy click para abrir la pestaña
                    sleep(random.uniform(4.0, 6.0))
                    userLink.click()

                    # Me muevo a la nueva pestaña
                    sleep(random.uniform(2.0, 4.0))
                    driver.switch_to.window(driver.window_handles[1])
                    

                    # Extraigo los datos
                    try:
                        title = driver.find_element(By.XPATH, "//div[@class='col-xxl-8']/h1").text
                        title = title.replace("\n", "").replace("\t", "").replace("\r", "").strip()
                    except:
                        title = None

                    seller = "Nocnok"
                    seller.strip()

                    try:
                        property_type = driver.find_element(By.XPATH, "//div[@id='type']//div[@class='col text-end']").text
                        property_type = property_type.strip() 
                    except:
                        property_type = None

                    try:
                        address = driver.find_element(By.XPATH, "//h3[@class='location-area-location']").text
                        address = address.strip()
                    except:
                        address = None

                    try:
                        price = driver.find_element(By.XPATH, "//h2[@class='price-area-price']").text
                        price = price.replace("$", "").replace(",", "").replace("MXN", "").strip()
                    except:
                        price = None

                    try:
                        bedrooms = driver.find_element(By.XPATH, "//div[@id='bedrooms']//div[@class='col text-end']").text
                        bedrooms = bedrooms.strip()
                    except:
                        bedrooms = None

                    try:
                        bathrooms = driver.find_element(By.XPATH, "//div[@id='fullBathrooms']//div[@class='col text-end']").text
                        bathrooms = bathrooms.strip()
                    except:
                        bathrooms = None

                    try:
                        built_area = driver.find_element(By.XPATH, "//div[@id='constructionSize']//div[@class='col text-end']").text
                        built_area = built_area.replace("m²", "").strip()
                    except:
                        built_area = None

                    try:
                        land_area = driver.find_element(By.XPATH, "//div[@id='lotSize'][1]//div[@class='col text-end']").text
                        land_area = land_area.replace("m²", "").strip()
                    except:
                        land_area = None

                    try:
                        parking = driver.find_element(By.XPATH, "//div[@class='icon-box']/span/i[@class='fa fa-car']/following-sibling::text()[1]").text
                        parking = parking.strip()
                    except:
                        parking = None

                    try:
                        description = driver.find_element(By.XPATH, "//p[@class='description']").text
                        description = description.replace("\n", "").replace("\t", "").replace("\r", "").strip()
                    except:
                        description = None



                    # title.replace("\n", "").replace("\t", "").replace("\r", "").strip()
                    # seller.strip()
                    # property_type.strip() 
                    # address.strip()
                    # price.replace("$", "").replace(",", "").replace("MXN", "").strip()
                    # bedrooms.strip()
                    # bathrooms.strip()
                    # built_area.replace("m²", "").strip()
                    # land_area.strip("m²", "").strip()
                    # description.replace("\n", "").replace("\t", "").replace("\r", "").strip()
                    
                    
                    print("title", title)
                    print("seller", seller)
                    print("property_type", property_type)
                    print("address", address)
                    print("price", price)
                    print("bedrooms", bedrooms)
                    print("bathrooms", bathrooms)
                    print("built_area", built_area)
                    print("land_area", land_area)
                    print("parking", parking)
                    print("description", description)

                    # Escribe una fila en el archivo CSV
                    writer.writerow([title, seller, property_type, address, price, bedrooms, bathrooms, built_area, land_area, parking, description])


                    # Ya que extraje todos los reviews del usuario, cierro la pestaña
                    sleep(random.uniform(1.0, 3.0))
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                except Exception as e:
                    print(e)
                    driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print(f"Falló la paginación")
            print(f"error{e}")


# Cerrar el navegador
driver.quit()





