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
driver.get(
    "https://inmuebles.mercadolibre.com.mx/casas/venta/oaxaca/oaxaca-de-juarez/#applied_filter_id%3DPROPERTY_TYPE%26applied_filter_name%3DInmueble%26applied_filter_order%3D1%26applied_value_id%3D242060%26applied_value_name%3DCasas%26applied_value_order%3D1%26applied_value_results%3D16%26is_custom%3Dfalse"
)
driver.maximize_window()

# Espero unos segundos después de que cargue la página
sleep(random.uniform(3.0, 5.0))


with open("casas_mercadoLibre.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Escribo la primera fila con los nombres de las columnas
    writer.writerow(
        [
            "title",
            "seller",
            "property_type",
            "address",
            "price",
            "bedrooms",
            "bathrooms",
            "built_Area",
            "land_Area",
            "parking",
            "description",
        ]
    )

    #  Acá me muevo a las pestañas donde están mis datos y los extraigo
    # -------------------------------------------------------------------
    reviews = driver.find_elements(By.XPATH, "//li[@class='ui-search-layout__item']")

    for review in reviews:
        try:
            # Me ubico en la parte en donde está el link para abrir la pesataña del usuario
            userLink = review
            sleep(random.uniform(3.0, 6.0))

            # Le doy click para abrir la pestaña
            userLink.click()

            # Me muevo a la nueva pestaña
            driver.switch_to.window(driver.window_handles[1])

            # Doy click al botón para cargar la sección con los datos a extraer
            boton_info = driver.find_element(
                By.XPATH, "//span[@class='ui-pdp-collapsable__action']"
            )
            driver.execute_script("arguments[0].scrollIntoView();", boton_info)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(boton_info))
            sleep(random.uniform(1.0, 2.0))
            boton_info.click()

            sleep(random.uniform(1.0, 2.0))

            # Extraigo los datos
            try:
                title = driver.find_element(
                    By.XPATH, "//h1[@class='ui-pdp-title']"
                ).text
                title = (
                    title.replace("\n", "").replace("\t", "").replace("\r", "").strip()
                )
            except:
                title = None

            seller = "MercadoLibre"
            seller.strip()

            try:
                property_type = driver.find_element(
                    By.XPATH,
                    "//tr[@class='andes-table__row ui-vpp-striped-specs__row' and th/div[text()='Tipo de casa']]/td/span",
                ).text
                property_type = property_type.strip()
            except:
                property_type = None

            try:
                address = driver.find_element(
                    By.XPATH,
                    "//div[@id='location']//div[@class='ui-pdp-media__body']/p",
                ).text
                address = address.strip()
            except:
                address = None

            try:
                price = driver.find_element(
                    By.XPATH, "//div[@class='ui-pdp-price__second-line']/span/span[3]"
                ).text
                price = (
                    price.replace("$", "").replace(",", "").replace("MXN", "").strip()
                )
            except:
                price = None

            try:
                bedrooms = driver.find_element(
                    By.XPATH,
                    "//tr[@class='andes-table__row ui-vpp-striped-specs__row' and th/div[text()='Recámaras']]/td/span",
                ).text
                bedrooms = bedrooms.strip()
            except:
                bedrooms = None

            try:
                bathrooms = driver.find_element(
                    By.XPATH,
                    "//tr[@class='andes-table__row ui-vpp-striped-specs__row' and th/div[text()='Baños']]/td/span",
                ).text
                bathrooms = bathrooms.strip()
            except:
                bathrooms = None

            try:
                built_area = driver.find_element(
                    By.XPATH,
                    "//tr[@class='andes-table__row ui-vpp-striped-specs__row' and th/div[text()='Superficie construida']]/td/span",
                ).text
                built_area = built_area.replace("m²", "").strip()
            except:
                built_area = None

            try:
                land_area = driver.find_element(
                    By.XPATH,
                    "//tr[@class='andes-table__row ui-vpp-striped-specs__row' and th/div[text()='Superficie total']]/td/span",
                ).text
                land_area = land_area.replace("m²", "").strip()
            except:
                land_area = None

            try:
                parking = driver.find_element(
                    By.XPATH,
                    "//tr[@class='andes-table__row ui-vpp-striped-specs__row' and th/div[text()='Estacionamientos']]/td/span",
                ).text
                parking = parking.strip()
            except:
                parking = None

            try:
                description = driver.find_element(
                    By.XPATH, "//div[@class='ui-pdp-description']/p"
                ).text
                description = (
                    description.replace("\n", "")
                    .replace("\t", "")
                    .replace("\r", "")
                    .strip()
                )
            except:
                description = None

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
            print("description", description, end="\n\n")

            # Escribe una fila en el archivo CSV
            writer.writerow(
                [
                    title,
                    seller,
                    property_type,
                    address,
                    price,
                    bedrooms,
                    bathrooms,
                    built_area,
                    land_area,
                    parking,
                    description,
                ]
            )

            # Ya que extraje todos los reviews del usuario, cierro la pestaña
            driver.close()
            sleep(random.uniform(2.0, 4.0))
            driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print(e)
            driver.switch_to.window(driver.window_handles[0])
