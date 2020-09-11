from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader


# Modelo de extraccion
class Pregunta(Item):
    titulo = Field()
    descripcion = Field()

# Clase para el spider
class StackOverflowSpider(Spider):
    name = "StackOverflowSpider"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }
    start_urls = ["https://stackoverflow.com/questions"]

    # Definimos la funcion que hace el parseo
    def parse(self, response):
        selc = Selector(response)
        preguntas = selc.xpath("//div[@id='questions']//div[contains(@class, 'question-summary')]")

        for pregunta in preguntas:
            item = ItemLoader(Pregunta(), pregunta)
            item.add_xpath('titulo', './/h3/a/text()')
            item.add_xpath('descripcion', './/div[@class="excerpt"]/text()')

            yield item.load_item()