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
    price  = Field()
    bedrooms = Field()
    bathrooms = Field()
    built_area = Field()
    land_area = Field()
    description = Field()
    publication_date = Field()


class MySpider(CrawlSpider):
    name = "propiedadesSpider"

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "FEED_EXPORT_FIELDS": ["title", "seller", "property_type", "address", "price", 
                               "bedrooms", "bathrooms", "built_area", "land_area", 
                               "description", "publication_date"]
    }

    download_delay = 5
    allowed_domains = ["casas.mitula.mx"]

    start_urls = ["https://casas.mitula.mx/casas/casas-oaxaca-juarez",
                  "https://casas.mitula.mx/casas/casas-oaxaca-juarez/2",
                  "https://casas.mitula.mx/casas/casas-oaxaca-juarez/3",
                  "https://casas.mitula.mx/casas/casas-oaxaca-juarez/4",
                  "https://casas.mitula.mx/casas/casas-oaxaca-juarez/5"]


    rules = (
        Rule(
            LinkExtractor(
                allow=r"/adform/.*"
            ), follow=True, callback="parse"
        ),
    )

    # Funciones para pasar como argunmento a MapCompose
    def price_fix(self, text):
        new_text = text.replace("\n", "").replace("\t", "").replace("MXN", "")\
            .replace("\r", "").replace("$", "").replace(",", "").strip()
        new_text = int(new_text)
        return new_text

    def bedrooms_fix(self, text):
        new_text = text.replace("\n", "").replace("\t", "").replace("\r", "")\
            .replace("recámaras", "").replace("recámara", "").strip()
        new_text = int(new_text)
        return new_text

    def bathrooms_fix(self, text):
        new_text = text.replace("\n", "").replace("\t", "").replace("\r", "")\
            .replace("baños", "").replace("baño", "").strip()
        new_text = int(new_text)
        return new_text

    def area_fix(self, text):
        new_text = text.replace("\n", "").replace("\t", "").replace("\r", "")\
            .replace("m²", "").replace(",", "").strip()
        new_text = int(new_text)
        return new_text

    def description_fix(self, text):
        new_text = text.replace("\n", "").replace("\t", "").replace("\r", "")\
            .replace("\xa0", "").strip()
        new_text = new_text
        return new_text


    def parse(self, response):
        sel = Selector(response)

        item = ItemLoader(Propiedad(), sel) 
        item.add_xpath("title", 
                       "//div[@class='main-title']/text()")
        item.add_value("seller", "Mitula")
        item.add_xpath("address", 
                       "//div[@class='location-map__location-address-map']/text()")
        item.add_xpath("price", 
                       "//div[@class='prices-and-fees__price']/text()",
                       MapCompose(self.price_fix))
        item.add_xpath("bedrooms", 
                       "//div[@class='details-item-icon' and i[@alt='bed']]/following-sibling::div/text()",
                       MapCompose(self.bedrooms_fix))
        item.add_xpath("bathrooms", 
                       "//div[@class='details-item-icon' and i[@alt='bath']]/following-sibling::div/text()",
                       MapCompose(self.bathrooms_fix))
        item.add_xpath("built_area", 
                       "//div[@class='details-item-icon' and i[@alt='area']]/following-sibling::div/text()",
                       MapCompose(self.area_fix))
        item.add_xpath("description", 
                       "//div[@id='description-text']/text()",
                       MapCompose(self.description_fix))
        item.add_xpath("publication_date", "//div[@class='date']/text()")
        features = sel.xpath("//div[@class='place-features']/div")
        for feature in features:
            feature_name = feature.xpath(".//span[1]/text()").get()
            feature_value = feature.xpath(".//span[2]/text()").get()
            if feature_name.strip() == "Tipo de vivienda:":
                item.add_value("property_type", feature_value)
            elif feature_name.strip() == "Superficie total:":
                item.add_value("land_area", feature_value,
                               MapCompose(self.area_fix))


        yield item.load_item()
        


process = CrawlerProcess({
"FEED_FORMAT": "csv",
"FEED_URI": "casas_mitula.csv"
})

process.crawl(MySpider)
process.start()