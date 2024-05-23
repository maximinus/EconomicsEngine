import itertools

from economics.offers import SellOffer, BuyOffer
from economics.errors import EconomyNoStockToRemove
from economics.heuristics import adjust_price_by_sales

HISTORY_MAX_LENGTH = 5


class Requirement:
    def __init__(self, product_id, total):
        self.product_id = product_id
        self.total = total


class Product:
    id_iter = itertools.count()

    def __init__(self, name, required=None):
        self.id = next(Product.id_iter)
        self.name = name
        if required is None:
            self.required = []
        else:
            self.required = required

    def requirement(self, total):
        return Requirement(self.id, total)

    def get_max_production(self, stock):
        # with this stock, return the most that can be produced
        max_production = None
        for requirement in self.required:
            if requirement.product_id not in stock:
                # we don't have this item
                return 0.0
            production_limit = stock[requirement.product_id] / requirement.total
            if max_production is None:
                max_production = production_limit
            else:
                if production_limit < max_production:
                    max_production = production_limit
        return max_production


# we need to remember what we sold and bought in the auctions, and the results
# therefore, we get a message every time we sell or buy something
class SellResult:
    def __init__(self, ask, actual, q, product):
        self.asking_price = ask
        self.actual_price = actual
        self.quantity = q
        self.product_id = product


class BuyResult:
    def __init__(self, offer, actual, q, product):
        self.offer_price = offer
        self.actual_price = actual
        self.quantity = q
        self.product_id = product


class ProducerCycleHistory:
    def __init__(self):
        self.auction_sales = []
        self.auction_buys = []
        self.sell_offers = []
        self.buy_offers = []


class Producer:
    id_iter = itertools.count()

    # a producer should only be able to adjust labor by a certain amount
    # let's start by having that fixed for now
    def __init__(self, product, money, stock=None):
        self.id = next(Producer.id_iter)
        self.product = product
        self.money = float(money)
        if stock is None:
            self.stock = {}
        else:
            self.stock = stock
        self.stock[self.product.id] = 0.0
        self.sale_price = 1.0
        self.last_consumption = {}
        self.cycle_history = []

    def consume_stock(self, production):
        # this has already been checked against stock
        # remove what we needed for the last production run
        # return what was consumed
        consumed = {}
        for required in self.product.required:
            amount_used = production * required.total
            self.stock[required.product_id] -= amount_used
            consumed[required.product_id] = amount_used
        return consumed

    def remove_stock(self, product_id, quantity):
        if product_id in self.stock:
            self.stock[product_id] -= quantity
        else:
            raise EconomyNoStockToRemove(f'Error: No product #{product_id} to remove')

    def add_stock(self, product_id, quantity):
        if product_id in self.stock:
            self.stock[product_id] += quantity
        else:
            self.stock[product_id] = quantity

    def init_cycle(self):
        # called at the start of a cycle
        self.cycle_history.append(ProducerCycleHistory())
        if len(self.cycle_history) > HISTORY_MAX_LENGTH:
            self.cycle_history.pop(0)

    def produce(self):
        # produce what we can, given our resources
        production = self.product.get_max_production(self.stock)
        self.last_consumption = self.consume_stock(production)
        self.stock[self.product.id] += production

    def get_sell_offers(self):
        # take all the stock we have and offer it for a price
        available_to_sell = self.stock[self.product.id]
        if available_to_sell == 0:
            return []
        offer = SellOffer(self, self.product.id, available_to_sell, self.sale_price)
        self.cycle_history[-1].sell_offers.append(offer.copy())
        return [offer]

    def get_buy_orders(self):
        # look at what we consumed and buy it back
        orders = []
        for product, total in self.last_consumption.items():
            buy = BuyOffer(self, product, total, 1.0)
            self.cycle_history[-1].buy_offers.append(buy.copy())
            orders.append(buy)
        return orders

    def add_sale(self, sale):
        self.cycle_history[-1].auction_sales.append(sale)

    def add_purchase(self, purchase):
        self.cycle_history[-1].auction_buys.append(purchase)

    def post_cycle(self, history):
        self.sale_price = adjust_price_by_sales(self, history)


class Workers(Producer):
    # workers are really just a special type of producer
    def __init__(self, total, labor, food_id):
        super().__init__(labor, 10, {food_id: total})
        self.id = next(Producer.id_iter)
        self.labor_id = labor.id
        self.desires = [food_id]
        self.workers = total

    def produce(self):
        pass

    def init_cycle(self):
        super().init_cycle()
        # workers eat food
        for i in self.desires:
            self.stock[i] -= self.workers

    def get_sell_offers(self):
        # the labor offer is the average cost of the worker
        # to start with, we handle this as a fixed cost
        # 1 unit of money per worker
        return [SellOffer(self, self.labor_id, self.workers, 1)]

    def get_buy_orders(self):
        # workers require 1 food per worker per cycle
        max_price = self.money / self.workers
        return [BuyOffer(self, self.desires[0], self.workers, max_price)]
