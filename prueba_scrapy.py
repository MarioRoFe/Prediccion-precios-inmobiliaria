from scrapy.item import Item, Field
from scrapy.spiders import CrawlSpider, Spider, Rule
from scrapy.selector import Selector
from itemloaders.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess


class Propiedad(Item):
    vendedor = Field()
    tipo_propiedad = Field()
    direccion = Field()
    precio  = Field()
    recamaras = Field()
    banios = Field()
    construccion_m2 = Field()
    terreno_m2 = Field()
    descripcion = Field()


class MySpider(CrawlSpider):
    name = "propiedadesSpider"

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5892.0 Safari/537.36",
        "FEED_EXPORT_FIELDS": ["vendedor", "tipo_propiedad", "direccion", "precio" ,"recamaras","banios","construccion_m2", "terreno_m2", "descripcion"]
    }

    download_delay = 5
    allowed_domains = ["casas.trovit.com.mx"]

    start_urls = ["https://casas.trovit.com.mx/casa-oaxaca-juarez/10"]



    rules = (
        # entrar y extraer
        Rule(
            LinkExtractor(
                allow=r"/listing/"
            ), follow=True, callback="parse"
        ),
    

        # Paginacion
        Rule(
            LinkExtractor(
                allow=r"casa-oaxaca-juarez/\d*"
            ), follow=True
        ),
    )



    def parse(self, response):
        sel = Selector(response)

        item = ItemLoader(Propiedad(), sel)
        item.add_value("vendedor", "Trovit")
        item.add_xpath("direccion", "//h2[@class='address']/text()")
        item.add_xpath("precio", "//div[@class='price']//span/text()")
        item.add_xpath("descripcion", "//div[@id='description']/p/text()")
        amenities = sel.xpath("//div[@id='amenities']//li")
        for amenitie in amenities:
            amenitie_name = amenitie.xpath("./div[1]/text()").get()
            amenitie_value = amenitie.xpath("./div[2]/text()").get()
            if amenitie_name.strip() == "Tipo de propiedad":
                item.add_value("tipo_propiedad", amenitie_value)
            elif amenitie_name.strip() == "Habitaciones":
                item.add_value("recamaras", amenitie_value)
            elif amenitie_name.strip() == "Baños":
                item.add_value("banios", amenitie_value)
            elif (amenitie_name.strip() == "Superficie") | (amenitie_name.strip() == "Superficie construida"):
                item.add_value("construccion_m2", amenitie_value)
            elif amenitie_name.strip() == "Superficie del terreno":
                item.add_value("terreno_m2", amenitie_value)
        

        yield item.load_item()
        


process = CrawlerProcess({
"FEED_FORMAT": "csv",
"FEED_URI": "casas_trovit.csv"
})

process.crawl(MySpider)
process.start()