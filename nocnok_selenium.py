import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



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
# Esto debido a que esta página tiene un comportamiento 
# un poco raro cuando carga. De esta manera me aseguro
# de que todo está listo para realizar mis acciones
sleep(random.uniform(5.0, 6.0))



#  Acá me muevo a las pestañas donde están mis datos y los extraigo
# --------------------------------------------------------------------

# Obtengo los botones para pasar entre páginas y los recorro con un for
sleep(random.uniform(2.0, 4.0))
botones_de_paginacion = driver.find_elements(By.XPATH, "//div[@class='col-xl-12 col-lg-12 col-md-12 col-sm-12']//ul//li[position() >= 2 and position() < last()]")
for conteo, boton_de_paginacion in enumerate(botones_de_paginacion):
    if conteo > 1:
        boton_de_paginacion.click()

    # Obtengo la ubicación de cada enlace para entrar al detalle de cada casa
    reviews = driver.find_elements(By.XPATH, "//div[@class='col-xxl-4 col-xl-4 col-lg-4 col-md-6 col-sm-6']")
    for review in reviews:
        # Me ubico en la parte en donde está el link para abrir la pesataña del usuario
        # userLink = review.find_element(By.XPATH, ".//div[@class='property-card-grid-wrap-details']/span/a")
        
        try:
            # Me ubico en la parte en donde está el link para abrir la pesataña del usuario
            sleep(random.uniform(5.0, 6.0))
            userLink = review.find_element(By.XPATH, ".//div[@class='property-card-grid-wrap-details']/span/a")
            
            # # Esperar a que el enlace sea clickeable antes de hacer clic
            # wait = WebDriverWait(driver, 10)
            # userLink = wait.until(EC.element_to_be_clickable((By.XPATH, ".//div[@class='property-card-grid-wrap-details']/span/a")))

            # Le doy click para abrir la pestaña
            sleep(random.uniform(5.0, 6.0))
            userLink.click()

            # # Esperar a que se abra la nueva pestaña
            # wait.until(EC.number_of_windows_to_be(2))

            sleep(random.uniform(2.0, 4.0))

            # Me muevo a la nueva pestaña
            driver.switch_to.window(driver.window_handles[1])
            

            # Extraigo los datos
            title = driver.find_element(By.XPATH, "//div[@class='col-xxl-8']/h1").text
            seller = "Nocnok"
            property_type = driver.find_element(By.XPATH, "//div[@id='type']//div[@class='col text-end']").text
            address = driver.find_element(By.XPATH, "//h3[@class='location-area-location']").text
            price = driver.find_element(By.XPATH, "//h2[@class='price-area-price']").text
            bedrooms = driver.find_element(By.XPATH, "//div[@id='bedrooms']//div[@class='col text-end']").text
            bathrooms = driver.find_element(By.XPATH, "//div[@id='fullBathrooms']//div[@class='col text-end']").text
            built_area = driver.find_element(By.XPATH, "//div[@id='constructionSize']//div[@class='col text-end']").text
            land_area = driver.find_element(By.XPATH, "//div[@id='lotSize'][1]//div[@class='col text-end']").text
            description = driver.find_element(By.XPATH, "//p[@class='description']").text

            print("title", title)
            print("seller", seller)
            print("property_type", property_type)
            print("address", address)
            print("price", price)
            print("bedrooms", bedrooms)
            print("bathrooms", bathrooms)
            print("built_area", built_area)
            print("land_area", land_area)
            print("description", description)


            # Ya que extraje todos los reviews del usuario, cierro la pestaña
            driver.close()
            sleep(random.uniform(3.0, 4.0))
            driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print(e)
            driver.switch_to.window(driver.window_handles[0])

