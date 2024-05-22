import unittest

from economics.producer import Product


class TestProduct(unittest.TestCase):
    def test_new_instance(self):
        _ = Product('Wood')
        _ = Product('Iron', [])

    def test_required(self):
        p = Product('Wood')
        self.assertEqual(len(p.required), 0)

    def test_max_production(self):
        a = Product('A')
        b = Product('B')
        c = Product('C', required=[a.requirement(2), b.requirement(3)])
        stock = {a:10, b: 6}
        self.assertEqual(c.get_max_production(stock), 2)
