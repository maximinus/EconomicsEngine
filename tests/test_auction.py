import unittest

from economics.producer import Product, Producer
from economics.offers import SellOffer, BuyOffer
from economics.auctions import SingleAuction, create_auctions


class TestSingleAuction(unittest.TestCase):
    def setUp(self):
        self.product = Product('a')
        self.seller = Producer(self.product, 10.0)
        self.buyer = Producer(self.product, 10.0)

    def test_null_auction(self):
        auction = SingleAuction()
        self.assertFalse(auction.valid)

    def test_no_buys(self):
        auction = SingleAuction()
        auction.sells.append(SellOffer(self.seller, self.product, 1.0, 1.0))
        self.assertFalse(auction.valid)

    def test_no_sales(self):
        auction = SingleAuction()
        auction.buys.append(BuyOffer(self.buyer, self.product, 1.0, 1.0))
        self.assertFalse(auction.valid)

    def test_single_sale(self):
        auction = SingleAuction()
        self.seller.money = 0.0
        self.buyer.money = 10.0
        auction.sells.append(SellOffer(self.seller, self.product, 1.0, 1.0))
        auction.buys.append(BuyOffer(self.buyer, self.product, 1.0, 1.0))
        auction.perform()
        self.assertEqual(self.seller.money, 1.0)

    def test_sale_transaction(self):
        auction = SingleAuction()
        self.seller.money = 0.0
        self.buyer.money = 10.0
        auction.sells.append(SellOffer(self.seller, self.product, 1.0, 1.0))
        auction.buys.append(BuyOffer(self.buyer, self.product, 1.0, 1.0))
        transactions = auction.perform()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].quantity, 1.0)

    def test_sell_price(self):
        # the sale proce should be the average of the buy and sell prices
        auction = SingleAuction()
        self.seller.money = 0.0
        self.buyer.money = 10.0
        auction.sells.append(SellOffer(self.seller, self.product, 1.0, 2.0))
        auction.buys.append(BuyOffer(self.buyer, self.product, 1.0, 10.0))
        transactions = auction.perform()
        # final price should be 10 + 2 / 2 -> 6
        self.assertEqual(transactions[0].price, 6.0)


class TestCreateAuctions(unittest.TestCase):
    # test a whole auction, with many products
    def setUp(self):
        self.wood = Product('Wood')
        self.iron = Product('Iron')
        self.wood_seller = Producer(self.wood, 10.0)

    def test_no_sales_one_auction(self):
        sells = [SellOffer(self.wood_seller, self.wood, 1.0, 1.0)]
        auctions = create_auctions(sells, [])
        self.assertEqual(len(auctions), 1)

    def test_no_buys_one_auction(self):
        buys = [BuyOffer(self.wood_seller, self.iron, 1.0, 1.0)]
        auctions = create_auctions([], buys)
        self.assertEqual(len(auctions), 1)

    def test_sales_correct_item(self):
        buys = [SellOffer(self.wood_seller, self.iron, 1.0, 1.0)]
        auctions = create_auctions([], buys)
        self.assertEqual(len(auctions), 1)
        self.assertTrue(self.iron in auctions)

    def test_buys_correct_item(self):
        buys = [BuyOffer(self.wood_seller, self.iron, 1.0, 1.0)]
        auctions = create_auctions([], buys)
        self.assertTrue(self.iron in auctions)
