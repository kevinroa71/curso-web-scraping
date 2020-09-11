# Importo las librerias
import requests
from lxml import html

# Url semilla y encabezados
url = "https://www.wikipedia.org/"
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

# peticion a la pagina
response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

# extraigo los idiomas del html
idiomas = dom.xpath("//a[starts-with(@id, 'js-link-box-')]/strong/text()")


print(idiomas)
