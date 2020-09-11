from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Instancio mi driver
driver = webdriver.Chrome('./chromedriver')

# Hago el requerimiento de la pagina
driver.get('https://www.olx.com.co/carros_c378')

for i in range(10):
    # Espero hasta que se cargue el boton
    boton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-aut-id='btnLoadMore']"))
    )

    if boton != None:
        # Hago click para cargar dinamicamente la informacion
        boton.click()

        # Espero a que se carguen los anuncios
        WebDriverWait(driver, 10).until_not(
            EC.presence_of_all_elements_located((By.XPATH, "//li[@class='_2JIfP']"))
        )

# Obtengo todos los autos
autos = driver.find_elements_by_xpath("//li[@data-aut-id='itemBox']")
for auto in autos:
    titulo = auto.find_element_by_xpath(".//span[@data-aut-id='itemTitle']").text
    price = auto.find_element_by_xpath(".//span[@data-aut-id='itemPrice']").text
    print(titulo)
    print(price)
