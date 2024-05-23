import unittest

from economics.history import History
from economics.offers import Transaction as Trans
from economics.producer import Product
from economics.auctions import SingleAuction

PRODUCT_A = Product('A')
PRODUCT_B = Product('B')
A_ID = PRODUCT_A.id
B_ID = PRODUCT_B.id


def get_auctions(trans):
    # trans is a list of lists
    all_auctions = []
    for trans_list in trans:
        auction = SingleAuction(trans_list[0].product_id)
        auction.transactions = trans_list
        all_auctions.append(auction)
    return all_auctions


class TestBaseStats(unittest.TestCase):
    def setUp(self):
        self.history = History()
        # for each cycle we give it some transactions. We'll give it 3
        # We need to pass some auctions
        cycle1 = get_auctions([[Trans(A_ID, 5, 6), Trans(A_ID, 3, 8)], [Trans(PRODUCT_B.id, 2, 5)]])
        cycle2 = get_auctions([[Trans(A_ID, 8, 7), Trans(A_ID, 9, 6)]])
        cycle3 = get_auctions([[Trans(A_ID, 3, 5), Trans(A_ID, 4, 6)], [Trans(PRODUCT_B.id, 2, 5)]])
        self.history.update(cycle1, [])
        self.history.update(cycle2, [])
        self.history.update(cycle3, [])

    def test_last_price(self):
        price = self.history.get_last_price(PRODUCT_A.id)
        self.assertAlmostEqual(price, 5.57, delta=0.01)

    def test_last_volume(self):
        volume = self.history.get_last_volume(PRODUCT_A.id)
        self.assertEqual(volume, 7)

    def test_last_range(self):
        price_range = self.history.get_last_price_range(PRODUCT_A.id)
        self.assertEqual(price_range.max_price, 6)
        self.assertEqual(price_range.min_price, 5)
