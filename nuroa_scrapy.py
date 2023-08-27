from scrapy.item import Item, Field
from scrapy.spiders import CrawlSpider, Spider, Rule
from scrapy.selector import Selector
from itemloaders.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess


class Propiedad(Item):
    precio = Field()


class MySpider(CrawlSpider):
    name = "propiedadesSpider"

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5892.0 Safari/537.36",
        "FEED_EXPORT_FIELDS": ["precio"]
    }

    download_delay = 5

    allowed_domains = ["www.nuroa.com.mx"]

    start_urls = ["https://www.nuroa.com.mx/venta-casas/casa-oaxaca"]


    rules = (
        Rule(
            LinkExtractor(
                allow=r"/adform/"
            ), follow=True, callback="parse"
        ),

        Rule(
            LinkExtractor(
                allow=r"page="
            ), follow=True
        ),
    )


    def parse(self, response):
        sel = Selector(response)

        
        item = ItemLoader(Propiedad(), sel)
        item.add_xpath("precio", "//div[@class='prices-and-fees__price']/text()")

        yield item.load_item()
        


process = CrawlerProcess({
"FEED_FORMAT": "csv",
"FEED_URI": "prueba.csv"
})

process.crawl(MySpider)
process.start()