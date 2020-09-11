# Importo las librerias
import requests
from bs4 import BeautifulSoup

# Url semilla y encabezados
url = "https://stackoverflow.com/questions"
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

# peticion a la pagina
response = requests.get(url, headers=headers)

# Parseamos la respuesta
soup = BeautifulSoup(response.text, features='lxml')
preguntas = soup.findAll('div', class_ = 'question-summary')

for pregunta in preguntas:
    title = pregunta.find('h3').text.strip()
    descr = pregunta.find('div', class_ = 'excerpt').text.strip()
    print(title)
    print(descr)
    print()