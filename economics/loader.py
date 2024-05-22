import json
import os.path

from economics.errors import EconomyLoadError
from economics.producer import Workers, Producer, Product, Requirement
from economics.economy import Economy

WORKER_TAG = 'workers'
PRODUCTS_TAG = 'products'
PRODUCERS_TAG = 'producers'
REQUIRED_TAG = 'requires'
LABOR_TAG = 'labor'
FOOD_TAG = 'food'
REQUIRED_PRODUCTS = [LABOR_TAG, FOOD_TAG]


def create_workers(worker_data, products):
    return Workers(float(worker_data['total']), products[LABOR_TAG], products[FOOD_TAG])


def create_products(product_data):
    products = {}
    for product_details in product_data:
        name = product_details['name']
        products[name] = Product(name)
    for single_product in REQUIRED_PRODUCTS:
        if single_product not in products:
            raise EconomyLoadError(f'Error: Missing required product {single_product}')
    # now add requirements
    for product_details in product_data:
        if REQUIRED_TAG in product_details:
            for require_data in product_details[REQUIRED_TAG]:
                for name, quantity in require_data.items():
                    r = Requirement(products[name], quantity)
                    products[product_details['name']].required.append(r)
    return products


def create_producers(producer_data, products):
    all_producers = []
    for single_producer in producer_data:
        starting_stock = {}
        for name, value in single_producer['stock'].items():
            starting_stock[products[name]] = value
        new_producer = Producer(products[single_producer['product']],
                                single_producer['money'],
                                starting_stock)
        all_producers.append(new_producer)
    return all_producers


def load_data_from_file(filepath):
    if not os.path.exists(filepath):
        raise EconomyLoadError(f'Path {filepath} does not exist')
    try:
        with open(filepath) as json_data:
            return json.load(json_data)
    except Exception as ex:
        raise EconomyLoadError(f'Error: {ex}')


def validate_data(data):
    for key in [WORKER_TAG, PRODUCTS_TAG, PRODUCERS_TAG]:
        if key not in data:
            raise EconomyLoadError(f'Error: Missing {key} in data')


def load_economy(filepath):
    data = load_data_from_file(filepath)
    validate_data(data)
    try:
        products = create_products(data[PRODUCTS_TAG])
        producers = create_producers(data[PRODUCERS_TAG], products)
        workers = create_workers(data[WORKER_TAG], products)
    except Exception as ex:
        raise EconomyLoadError(f'Error: {ex}')
    producers.insert(0, workers)
    return Economy([x for x in products.values()], producers)
