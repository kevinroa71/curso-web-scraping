from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Inicializo el driver
opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
)
driver = webdriver.Chrome('./chromedriver', options = opts)


# Abro url semilla
driver.get("https://listado.mercadolibre.com.ve/perros-cachorros/cachorros-bulldog")


# Hago la paginacion y extraigo todas las urls verticales
links = []
while True:
    # extraigo los elementos de la pagina actual
    items = driver.find_elements(By.XPATH, "//li[@class='ui-search-layout__item']//div[@class='ui-search-result__image']/a")
    for item in items:
        links.append(item.get_attribute('href'))

    # Hago click en siguiente si no estoy en la ultima pagina
    try:
        siguiente = driver.find_element_by_xpath("//a[@title='Siguiente']")
        driver.get(siguiente.get_attribute('href'))
    except Exception as e:
        break

for link in links:
    driver.get(link)
    try:
        title = driver.find_element_by_xpath("//h1[contains(@class, 'item-title__primary')]").text
        precio = driver.find_element_by_xpath("//fieldset[contains(@class, 'item-price')]//span[contains(@class, 'price-tag-fraction')]").text
        print(title)
        print(precio)
    except Exception as e:
        print(e)
