from requests import get
from requests.auth import HTTPBasicAuth
from pydantic import BaseModel, validator
from typing import List

import urllib
import json
import sys

# Assumptions: All categories for a brand must have items, if it returns
#              an empty item list, an error is raised
# Description: The programs takes a brand and a category and spits out the
#              most expensive and cheapest product in the catalogue


class Product(BaseModel):
    brand: str
    sub_brand: str
    department: str
    category: str
    product_name: str
    barcode: str
    cost: str


class Filter(BaseModel):
    current_page: str
    brand: str
    category: str


class Barcode_Response(BaseModel):
    filter: Filter
    items: List[str]

    @validator("items")
    def check_items_exists(cls, v):
        if len(v) == 0:
            raise ValueError("items do not exists based on the given filters")
        return v


class WingTaiService:
    def __init__(self, username, password):
        self.auth = HTTPBasicAuth(username, password)
        self.endpoint = "https://wingtai.io"

    def send_get_request(self, url, params=None):
        try:
            rest_client = get(url, params=params, auth=self.auth)
            rest_client.raise_for_status()
            return rest_client.content
        except Exception as e:
            print(e)

    def get_barcodes_from_brand_and_category(
        self, brand, category, sort_direction, current_page=1, sort_key="cost"
    ):
        # encodes each query string
        parameter = {
            "brand": brand,
            "category": category,
            "current_page": current_page,
            "sort_key": sort_key,
            "sort_direction": sort_direction,
        }
        params = urllib.parse.urlencode(parameter, quote_via=urllib.parse.quote)

        # construct the url
        url = f"{self.endpoint}/rest/barcodes"
        content = self.send_get_request(url, params)
        return Barcode_Response(**json.loads(content))

    def get_product_from_barcode(self, response):
        # encodes the brand and construct the url
        url = f"{self.endpoint}/rest/product/{urllib.parse.quote(response.filter.brand)}/{response.items[0]}"
        content = self.send_get_request(url)
        product = Product(**json.loads(content))
        return product

    def prepare_output_format(self, products):
        output = {
            "bottom": {
                "barcode": products[0].barcode,
                "cost": products[0].cost,
            },
            "top": {
                "barcode": products[1].barcode,
                "cost": products[1].cost,
            },
        }
        return json.dumps(output)

    def get_top_bottom_product(self, brand, category):
        products = []
        for sorting_order in ["asc", "desc"]:
            response = self.get_barcodes_from_brand_and_category(
                brand, category, sorting_order
            )
            products.append(self.get_product_from_barcode(response))
        return self.prepare_output_format(products)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(len(sys.argv))
        print("example of usage: python question2.py FOX 'FAC KB PYJAMAS'")
    else:
        wingtai_service = WingTaiService("interview", "pos97HN345")
        print(
            f"output: {wingtai_service.get_top_bottom_product(sys.argv[1], sys.argv[2])}"
        )
