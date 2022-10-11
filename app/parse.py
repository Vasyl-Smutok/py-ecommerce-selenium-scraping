import csv

from dataclasses import dataclass, astuple
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By


BASE_URL = "https://webscraper.io/"
HOME_URL = urljoin(BASE_URL, "test-sites/e-commerce/more/")
COMPUTERS_URL = urljoin(HOME_URL, "computers/")
LAPTOPS_URL = urljoin(COMPUTERS_URL, "laptops")
TABLES_URL = urljoin(COMPUTERS_URL, "tablets")
PHONES_URL = urljoin(HOME_URL, "phones/")
TOUCH_URL = urljoin(PHONES_URL, "touch")

PRODUCT_FIELDS = ["title", "description", "price", "rating", "num_of_reviews"]

ALL_URLS = [HOME_URL, COMPUTERS_URL, LAPTOPS_URL,  TABLES_URL, PHONES_URL, TOUCH_URL]

driver = webdriver.Chrome()


@dataclass
class Product:
    title: str
    description: str
    price: float
    rating: int
    num_of_reviews: int


def parse_single_product(product_soup) -> Product:
    title = product_soup.find_element(By.CLASS_NAME, "title").text
    print(title)
    description = product_soup.find_element(By.CLASS_NAME, "description").text
    price = float(product_soup.find_element(By.CLASS_NAME, "price").text.replace("$", ""))
    rating = 2
    num_of_reviews = 2

    return Product(
        title=title,
        description=description,
        price=price,
        rating=rating,
        num_of_reviews=num_of_reviews,
    )


def get_single_page_product() -> list[Product]:
    products = driver.find_elements(By.CLASS_NAME, "col-md-4")
    return [parse_single_product(product) for product in products]


def get_all_products_in_page() -> list[Product]:
    all_products = get_single_page_product()

    return all_products


def get_all_products():
    for url in ALL_URLS:
        driver.get(url)

        cookies = driver.find_elements(By.CLASS_NAME, "acceptCookies")
        if cookies:
            cookies[0].click()

        more = driver.find_elements(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/a")

        # try:
        #     more[0]
        # except:
        #     more = []

        while more:
            if more[0].is_displayed():
                more[0].click()

            more = driver.find_elements(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/a")
            try:
                more[0].click()
            except:
               more = None

        name_csv_file = url.split("/")[-2] if url.split("/")[-2] != "more" else "home"

        with open(f"../data/{name_csv_file}.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(PRODUCT_FIELDS)
            products = get_all_products_in_page()
            writer.writerows(astuple(product) for product in products)


if __name__ == "__main__":
    get_all_products()
    driver.close()
