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
    parking = Field()


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
            "parking",
        ],
    }
    download_delay = 5
    allowed_domains = ["www.bienesraicesarletteescobar.com.mx"]
    start_urls = [
        "https://www.bienesraicesarletteescobar.com.mx/properties/mexico/oaxaca/oaxaca-de-juarez?page=1&web_page=properties"
    ]

    rules = (
        Rule(LinkExtractor(allow=r"/property/.*"), follow=True, callback="parse"),
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
            "title", "//h1[@class='title']/text()", MapCompose(self.spaces_fix)
        )
        item.add_xpath(
            "property_type",
            "//td[text()='Tipo:']/following-sibling::td/text()",
            MapCompose(self.spaces_fix),
        )
        item.add_value("seller", "arlette", MapCompose(self.spaces_fix))
        item.add_xpath("address", "//h2/a[1]/text()", MapCompose(self.spaces_fix))
        item.add_xpath(
            "price", "//div[@id='prices']//span/text()", MapCompose(self.price_fix)
        )
        item.add_xpath(
            "bedrooms",
            "//div[@id='main_features']//li[@class='beds']/text()",
            MapCompose(self.bedrooms_fix),
        )
        item.add_xpath(
            "bathrooms",
            "//div[@id='main_features']//li[@class='baths']/text()",
            MapCompose(self.bathrooms_fix),
        )
        item.add_xpath(
            "parking",
            "//td[text()='Estacionamientos:']/following-sibling::td/text()",
            MapCompose(self.spaces_fix),
        )
        item.add_xpath(
            "built_area",
            "//td[text()='Construcción:']/following-sibling::td/text()",
            MapCompose(self.area_fix),
        )
        item.add_xpath(
            "land_area",
            "//td[text()='Terreno:']/following-sibling::td/text()",
            MapCompose(self.area_fix),
        )
        item.add_xpath(
            "description",
            "//div[@id='description']//div[@class='info']/text()",
            MapCompose(self.description_fix),
        )

        yield item.load_item()


process = CrawlerProcess({"FEED_FORMAT": "csv", "FEED_URI": "casas_arlette.csv"})

process.crawl(MySpider)
process.start()
