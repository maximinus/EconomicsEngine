import unittest

from economics.history import History
from economics.offers import Transaction as Trans
from economics.producer import Product
from economics.auctions import SingleAuction

PRODUCT_A = Product('A')
PRODUCT_B = Product('B')


def get_auctions(trans):
    # trans is a list of lists
    all_auctions = []
    for trans_list in trans:
        auction = SingleAuction(trans_list[0].product)
        auction.transactions = trans_list
        all_auctions.append(auction)
    return all_auctions


class TestBaseStats(unittest.TestCase):
    def setUp(self):
        self.history = History()
        # for each cycle we give it some transactions. We'll give it 3
        cycle1 = get_auctions([[Trans(PRODUCT_A, 5, 6), Trans(PRODUCT_A, 3, 8)], [Trans(PRODUCT_B, 2, 5)]])
        cycle2 = get_auctions([[Trans(PRODUCT_A, 8, 7), Trans(PRODUCT_A, 9, 6)]])
        cycle3 = get_auctions([[Trans(PRODUCT_A, 3, 5), Trans(PRODUCT_A, 4, 6)], [Trans(PRODUCT_B, 2, 5)]])
        self.history.update(cycle1)
        self.history.update(cycle2)
        self.history.update(cycle3)

    def test_last_price(self):
        price = self.history.get_last_price(PRODUCT_A)
        self.assertAlmostEqual(price, 5.57, delta=0.01)

    def test_last_volume(self):
        volume = self.history.get_last_volume(PRODUCT_A)
        self.assertEqual(volume, 7)

    def test_last_range(self):
        price_range = self.history.get_last_price_range(PRODUCT_A)
        self.assertEqual(price_range.max_price, 6)
        self.assertEqual(price_range.min_price, 5)

    def test_historical_price(self):
        price = self.history.get_long_term_price(PRODUCT_A, 3)
        self.assertAlmostEqual(price, 6.26, delta=0.01)

    def test_historical_volume(self):
        volume = self.history.get_long_term_volume(PRODUCT_A, 3)
        self.assertAlmostEqual(volume, 10.67, delta=0.01)

    def test_range_overflow_price(self):
        price = self.history.get_long_term_price(PRODUCT_A, 10)
        self.assertAlmostEqual(price, 6.26, delta=0.01)

    def test_single_cycle_price(self):
        price = self.history.get_long_term_price(PRODUCT_A, 1)
        self.assertAlmostEqual(price, 5.57, delta=0.01)

    def test_missing_cycle_price(self):
        price = self.history.get_long_term_price(PRODUCT_B, 3)
        self.assertEqual(price, 5)

    def test_history_for_missing(self):
        product_history = self.history.get_product_history(PRODUCT_B, 3)
        self.assertIsNone(product_history[1])

    def history_length(self):
        product_history = self.history.get_product_history(PRODUCT_B, 3)
        self.assertEqual(len(product_history), 3)
