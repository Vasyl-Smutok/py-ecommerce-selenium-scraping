import csv
from dataclasses import dataclass, astuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://webscraper.io/"
HOME_URL = urljoin(BASE_URL, "test-sites/e-commerce/more/")
PRODUCT_FIELDS = ["title", "description", "price", "rating", "num_of_reviews"]


@dataclass
class Product:
    title: str
    description: str
    price: str
    rating: str
    num_of_reviews: str


def parse_single_product(product_soup) -> Product:
    title = product_soup.select_one(".title").text
    description = product_soup.select_one(".description").text
    price = product_soup.select_one(".price").text
    rating = "12"
    num_of_reviews = "122"

    return Product(
        title=title,
        description=description,
        price=price,
        rating=rating,
        num_of_reviews=num_of_reviews
    )


def get_single_page_product(page_soup: BeautifulSoup) -> list[Product]:
    products = page_soup.select(".col-md-4")
    return [parse_single_product(product) for product in products]


def get_all_products_in_home_page() -> list[Product]:
    page = requests.get(HOME_URL).content
    page_soup = BeautifulSoup(page, "html.parser")

    all_products = get_single_page_product(page_soup)
    print(all_products)

    return all_products


def get_all_products():
    with open('products.csv', "w") as file:
        writer = csv.writer(file)
        writer.writerow(PRODUCT_FIELDS)
        products = get_all_products_in_home_page()
        writer.writerows(astuple(product) for product in products)


if __name__ == "__main__":
    get_all_products()
