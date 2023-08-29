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

reviews = driver.find_elements(By.XPATH, "//div[@class='col-xxl-4 col-xl-4 col-lg-4 col-md-6 col-sm-6']")

for review in reviews:
    # Me ubico en la parte en donde está el link para abrir la pesataña del usuario
    userLink = review.find_element(By.XPATH, ".//div[@class='property-card-grid-wrap-details']/span/a")
    sleep(random.uniform(5.0, 8.0))
    try:
        # Le doy click para abrir la pestaña
        userLink.click()
        # Me muevo a la pestaña recién abierta
        # driver.window_handles contiene una lista con las ventanas 
        # que están abiertas mediante el driver de selenium. 
        # Con el índice le indico a cuál moverse

        # Me aseguro de estar en la sección de opiniones y no en la de fotos
        # Para esto hago click en opiniones
        # boton_opiniones = WebDriverWait(driver=driver, timeout=10).until(
        #     EC.presence_of_element_located((By.XPATH, "//button[@class='link read_more show']"))
        # )
        # boton_opiniones.click()


        # Me muevo a la nueva pestaña
        driver.switch_to.window(driver.window_handles[1])

        # Extraigo los datos
        precio = driver.find_element(By.XPATH, "//h2[@class='price-area-price']").text
        descripcion = driver.find_element(By.XPATH, "//p[@class='description']").text
        print(precio)
        print(descripcion, end="\n\n")

        # Ya que extraje todos los reviews del usuario, cierro la pestaña
        driver.close()
        sleep(random.uniform(3.0, 4.0))
        driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print(e)
        driver.switch_to.window(driver.window_handles[0])

driver.close()