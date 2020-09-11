from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose
import re


class Articulo(Item):
    nombre = Field()
    descripcion = Field()
    precio = Field()


class MercadoLibreCrawler(CrawlSpider):
    name = "MercadoLibreCrawler"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'DOWNLOAD_DELAY': 2,
        'CLOSESPIDER_PAGECOUNT': 500
    }

    allowed_domains = ['celulares.mercadolibre.com.ve', 'articulo.mercadolibre.com.ve']
    start_urls = ['https://celulares.mercadolibre.com.ve/']

    rules = (
        Rule(LinkExtractor(allow=r'/MLV-\d+', allow_domains=['articulo.mercadolibre.com.ve']), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=r'/_Desde_\d+', allow_domains=['celulares.mercadolibre.com.ve']), follow=True),
    )

    def parse_item(self, response):
        item = ItemLoader(Articulo(), response)

        item.add_xpath('nombre', '//h1[contains(@class, "item-title__primary")]/text()', MapCompose(self.clear_text))
        item.add_xpath('precio', '//fieldset[contains(@class, "item-price")]//span[contains(@class, "price-tag-fraction")]/text()', MapCompose(self.clear_price))
        item.add_xpath('descripcion', '//div[contains(@class, "item-description__text")]/p/text()', MapCompose(self.clear_text))

        yield item.load_item()

    def clear_text(self, texto):
        return texto.replace('\n', '').replace('\t', '').replace('\r', '').strip();

    def clear_price(self, price):
        return re.sub(pattern=r'[^\d]', repl='', string=self.clear_text(price))