import scrapy
import re
import json
from scrapy.crawler import CrawlerProcess


class ImmowebSpider(scrapy.Spider):
    """
    ImmowebSpider class is an instance of scrapy.Spider class
    contains 3 methods configured based on the order of execution indicated by callback parameter inside each method's yield statement
    """
    name = "immowebspider"
    allowed_domains = ["immoweb.be"]

    def start_requests(self):
        """
        default scrapy method to request the urls in 'url' variable, then yielding the response to the page_parser() method.
        """
        urls = (
            [
                f"https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={num}&orderBy=relevance"
                for num in range(1, 334)
            ]
            + [
                f"https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page={num}&orderBy=relevance"
                for num in range(1, 334)
            ]
            + [
                f"https://www.immoweb.be/en/search/house/for-rent?countries=BE&page={num}&orderBy=relevance"
                for num in range(1, 334)
            ]
            + [
                f"https://www.immoweb.be/en/search/apartment/for-rent?countries=BE&page={num}&orderBy=relevance"
                for num in range(1, 334)
            ]
        )
        for url in urls:
            yield scrapy.Request(url=url, callback=self.page_parser)

    def page_parser(self, response):
        """
        This method is designed to process the responsed urls from start_request() method by extracting the urls linked to 
        each classified's page followed by initiating request to those urls, then yielding the response to classified_parser() methhod  
        """
        classified_links = response.xpath(
            "//a[@class='card__title-link']/@href"
        ).extract()
        for link in classified_links:
            yield response.follow(url=link, callback=self.classified_parser)

    def classified_parser(self, response):
        script_text = response.xpath(
            "//script[contains(text(), 'window.classified =')]/text()" 
        ).get() # to fetch the text element inside <script> tag that begins with 'window.classified'
        json_str = re.search(
            r"window\.classified\s*=\s*(\{.*?\});", script_text, re.DOTALL
        ).group(1) # regular expression pattern to exclude 'windows.classified = ' in a literal way
        data_dict = {} # dictionary acting as a container of all scraped data.
        try:
            data_source = json.loads(json_str)
            data_dict["immo_code"] = data_source["id"]
            data_dict["immo_status"] = data_source["transaction"].get("type", "UNKNOWN")
            data_dict["epc_score"] = data_source["transaction"]["certificates"].get(
                "epcScore", "UNKNOWN"
            )
            data_dict["price"] = data_source["price"].get("mainValue", "UNKNOWN")
            data_dict["publication_date"] = data_source["publication"]["creationDate"][:10]
            data_dict["realtor_poc"] = data_source["customers"][0].get("name", "UNKNOWN")
            data_dict["listing_type"] = data_source["property"].get("type", "-")
            data_dict["listing_subtype"] = data_source["property"].get("subtype", "-")
            location = data_source["property"].get("location", "None")
            if location:
                data_dict["street"] = location.get("street", "-")
                data_dict["number"] = location.get("number", "-")
                data_dict["box"] = location.get("box", "-")
                data_dict["postcode"] = location.get("postalCode", "-")
                data_dict["locality"] = location.get("locality", "-")
                data_dict["district"] = location.get("district", "-")
                data_dict["province"] = location.get("province", "-")
                data_dict["region"] = location.get("region", "-")
                data_dict["listing_address"] = f"{data_dict['street']} {data_dict['number']} {data_dict['box']}"
            building = data_source["property"].get("building")
            if building:
                data_dict["construction_year"] = building.get(
                    "constructionYear", "UNKNOWN"
                )
                data_dict["condition"] = building.get("condition", "UNDETERMINED")
            land = data_source["property"]["land"]
            if land:
                data_dict["plot_size"] = land.get("surface", 0)
            data_dict["habitable_surface"] = data_source["property"].get(
                "netHabitableSurface", 0
            )
            data_dict["garden_surface"] = data_source["property"].get("gardenSurface", 0)
            data_dict["bedroom_count"] = data_source["property"].get("bedroomCount", 0)
            data_dict["bathroom_count"] = data_source["property"].get(
                "bathroomCount", 0
            )
            data_dict["toilet_count"] = data_source["property"].get("toiletCount", 0)
            data_dict["room_count"] = data_source["property"].get("roomCount", 0)
            data_dict["has_lift"] = data_source["property"].get("hasLift", False)
            data_dict["has_basement"] = data_source["property"].get(
                "hasBasement", False
            )
            data_dict["dining_room"] = data_source["property"].get("hasDiningRoom", "UNKNOWN")
            data_dict["kitchen"] = data_source["property"]["kitchen"].get(
                "type", "UNKNOWN"
            )
            data_dict["has_disabled_access"] = data_source["property"].get(
                "hasDisabledAccess", False
            )
            data_dict["has_internet"] = data_source["property"].get("hasInternet", False)
            data_dict["listing_desc"] = data_source["property"].get("title", "No Description Fund")
            data_dict["to_remove"] = "GOOD TO GO" 
        
        except Exception as err:
            
            data_dict["to_remove"] = "REMOVE ME"
            print(f"Error found in {response}: {err}")
        column_names = [
            "immo_code",
            "url"
            "immo_status",
            "price",
            "publication_date",
            "listing_type",
            "listing_subtype",
            "listing_address",
            "postcode",
            "locality",
            "district",
            "province",
            "region",
            "epc_score",
            "construction_year",
            "condition",
            "plot_size",
            "habitable_surface",
            "garden_surface",
            "bedroom_count",
            "bathroom_count",
            "toilet_count",
            "room_count",
            "kitchen",
            "dining_room",
            "has_lift",
            "has_basement",
            "has_internet",
            "has_disabled_access",
            "realtor_poc",
            "listing_desc",
            "to_remove"
        ]
        data_dict_ret = {}
        for colname in column_names:
            data_dict_ret[colname] = data_dict.get(colname)
        yield data_dict_ret

process = CrawlerProcess(
    settings={
        "FEEDS": {
            "dataset2.json": {"format": "json"},
        },
    }
)

process.crawl(ImmowebSpider)
process.start()  