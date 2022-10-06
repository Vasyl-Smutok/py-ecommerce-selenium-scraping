import csv
from dataclasses import dataclass, astuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://webscraper.io/"
HOME_URL = urljoin(BASE_URL, "test-sites/e-commerce/more/")
COMPUTERS_URL = urljoin(HOME_URL, "computers/")
LAPTOPS_URL = urljoin(HOME_URL, "laptops/")
TABLES_URL = urljoin(HOME_URL, "tables/")
PHONES_URL = urljoin(HOME_URL, "phones/")
TOUCH_URL = urljoin(HOME_URL, "touch/")

PRODUCT_FIELDS = ["title", "description", "price", "rating", "num_of_reviews"]

ALL_URLS = [HOME_URL, COMPUTERS_URL, LAPTOPS_URL, TABLES_URL, PHONES_URL, TOUCH_URL]


@dataclass
class Product:
    title: str
    description: str
    price: float
    rating: int
    num_of_reviews: int


def parse_single_product(product_soup) -> Product:
    title = product_soup.select_one(".title").attrs["title"]
    description = product_soup.select_one(".description").text
    price = float(product_soup.select_one(".price").text.replace("$", ""))
    rating = int(
        product_soup.select_one(".ratings > p:nth-child(2)").attrs["data-rating"]
    )
    num_of_reviews = int(
        product_soup.select_one(".ratings > p:nth-child(1)").text.split()[0]
    )

    return Product(
        title=title,
        description=description,
        price=price,
        rating=rating,
        num_of_reviews=num_of_reviews,
    )


def get_single_page_product(page_soup: BeautifulSoup) -> list[Product]:
    products = page_soup.select(".col-md-4")
    return [parse_single_product(product) for product in products]


def get_all_products_in_page(url) -> list[Product]:
    page = requests.get(url).content
    page_soup = BeautifulSoup(page, "html.parser")

    all_products = get_single_page_product(page_soup)

    return all_products


def get_all_products():
    for url in ALL_URLS:
        name_csv_file = url.split("/")[-2] if url.split("/")[-2] != "more" else "home"

        with open(f"../data/{name_csv_file}.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(PRODUCT_FIELDS)
            products = get_all_products_in_page(url)
            writer.writerows(astuple(product) for product in products)


if __name__ == "__main__":
    get_all_products()
