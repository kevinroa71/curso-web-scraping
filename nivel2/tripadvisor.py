from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
import re



class Hotel(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    ventajas = Field()


class TripAdvisor(CrawlSpider):
    name = "TripAdvisor"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'DOWNLOAD_DELAY': 2
    }
    start_urls = ["https://www.tripadvisor.com.ve/Hotels-g294074-Bogota-Hotels.html"]

    rules = (Rule(LinkExtractor(allow=r'/Hotel_Review-'), follow=True, callback="parse_hotel"),)

    def parse_hotel(self, response):
        selc = Selector(response)
        item = ItemLoader(Hotel(), selc)

        item.add_xpath('nombre', '//h1[@id="HEADING"]/text()')
        item.add_xpath('precio', '//div[@class="CEf5oHnZ"]/text()', MapCompose(self.limpiarPrecio))
        item.add_xpath('descripcion', '//div[@class="cPQsENeY"][1]/text()')
        item.add_xpath('ventajas', '//div[@data-test-target="amenity_text"]/text()')

        yield item.load_item()

    def limpiarPrecio(self, precio):
        return re.sub(pattern=r'[^\d]', repl='', string=precio)