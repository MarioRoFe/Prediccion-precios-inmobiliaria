from scrapy.item import Item, Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from itemloaders.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess


class Propiedad(Item):
    title = Field()
    seller = Field()
    property_type = Field()
    address = Field()
    price = Field()
    bedrooms = Field()
    bathrooms = Field()
    built_area = Field()
    land_area = Field()
    description = Field()
    publication_date = Field()


class MySpider(CrawlSpider):
    name = "propiedadesSpider"

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5892.0 Safari/537.36",
        "FEED_EXPORT_FIELDS": [
            "title",
            "seller",
            "property_type",
            "address",
            "price",
            "bedrooms",
            "bathrooms",
            "built_area",
            "land_area",
            "description",
            "publication_date",
        ],
        "ROBOTSTXT_OBEY": False,
    }

    download_delay = 3

    allowed_domains = ["www.lamudi.com.mx"]

    start_urls = ["https://www.lamudi.com.mx/oaxaca/oaxaca-de-juarez/casa/for-sale/"]

    rules = (
        # entrar y extraer
        Rule(LinkExtractor(allow=r"/detalle/.*"), follow=True, callback="parse"),
        # Paginación
        Rule(LinkExtractor(allow=r"page=.*"), follow=True),
    )

    # Funciones para pasar como argunmento a MapCompose
    def price_fix(self, text):
        new_text = (
            text.replace("\n", "")
            .replace("\t", "")
            .replace("MXN", "")
            .replace("\r", "")
            .replace("$", "")
            .replace(",", "")
            .strip()
        )
        new_text = int(new_text)
        return new_text

    def bedrooms_fix(self, text):
        new_text = (
            text.replace("\n", "")
            .replace("\t", "")
            .replace("\r", "")
            .replace("recámaras", "")
            .replace("recámara", "")
            .strip()
        )
        new_text = int(new_text)
        return new_text

    def bathrooms_fix(self, text):
        new_text = (
            text.replace("\n", "")
            .replace("\t", "")
            .replace("\r", "")
            .replace("baños", "")
            .replace("baño", "")
            .strip()
        )
        new_text = int(new_text)
        return new_text

    def area_fix(self, text):
        new_text = (
            text.replace("\n", "")
            .replace("\t", "")
            .replace("\r", "")
            .replace("m²", "")
            .replace(",", "")
            .strip()
        )
        new_text = int(new_text)
        return new_text

    def description_fix(self, text):
        new_text = (
            text.replace("\n", "")
            .replace("\t", "")
            .replace("\r", "")
            .replace("\xa0", "")
            .strip()
        )
        new_text = new_text
        return new_text

    def spaces_fix(self, text):
        new_text = text.strip()
        new_text = new_text
        return new_text

    def parse(self, response):
        sel = Selector(response)
        item = ItemLoader(Propiedad(), sel)

        item.add_xpath(
            "title", "//div[@class='main-title']/h1/text()", MapCompose(self.spaces_fix)
        )
        item.add_value("seller", "lamudi")
        item.add_xpath(
            "address", "//div[@id='view-map__text']/text()", MapCompose(self.spaces_fix)
        )
        item.add_xpath(
            "price",
            "//div[@class='prices-and-fees__price']/text()",
            MapCompose(self.price_fix),
        )
        item.add_xpath(
            "bedrooms",
            "//div[@class='details-item' and .//i[@title='bed']]//div[@class='details-item-value']/text()",
            MapCompose(self.bedrooms_fix),
        )
        item.add_xpath(
            "bathrooms",
            "//div[@class='details-item' and .//i[@title='bath']]//div[@class='details-item-value']/text()",
            MapCompose(self.bathrooms_fix),
        )
        item.add_xpath(
            "built_area",
            "//div[@class='details-item' and .//i[@title='area']]//div[@class='details-item-value']/text()",
            MapCompose(self.area_fix),
        )
        item.add_xpath(
            "land_area",
            "//div[@class='plot-area']/span[@class='place-features__values']/text()",
            MapCompose(self.area_fix),
        )
        item.add_xpath(
            "description",
            "//div[@id='description-text']/text()",
            MapCompose(self.description_fix),
        )
        item.add_xpath(
            "publication_date",
            "//div[@class='date']/text()",
            MapCompose(self.spaces_fix),
        )
        item.add_xpath(
            "property_type",
            "//div[@class='property-type']/span[2]/text()",
            MapCompose(self.spaces_fix),
        )

        yield item.load_item()


process = CrawlerProcess({"FEED_FORMAT": "csv", "FEED_URI": "casas_lamudi.csv"})

process.crawl(MySpider)
process.start()
