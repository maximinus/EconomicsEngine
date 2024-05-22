import unittest
from pathlib import Path

from economics.loader import load_economy
from economics.economy import Economy
from economics.producer import Workers


BASIC_CONFIG = Path('../examples/basic.json')


class TestBasicExample(unittest.TestCase):
    def setUp(self):
        self.economy = load_economy(BASIC_CONFIG)

    def test_exists(self):
        self.assertTrue(isinstance(self.economy, Economy))

    def test_has_two_producers(self):
        self.assertEqual(len(self.economy.producers), 2)

    def test_has_two_products(self):
        self.assertEqual(len(self.economy.products), 2)

    def test_first_producer_is_worker(self):
        self.assertTrue(isinstance(self.economy.producers[0], Workers))

    def test_producer_has_requirements(self):
        food_maker = self.economy.producers[1]
        food_product = food_maker.product
        self.assertTrue(len(food_product.required) > 0)
