from economics.offers import SellOffer, BuyOffer
from economics.errors import EconomyNoStockToRemove


class Requirement:
    def __init__(self, product, total):
        self.product = product
        self.total = total


class Workers:
    # workers are really just a special type of producer
    def __init__(self, total, labor, food):
        self.labor = labor
        self.desires = [food]
        self.total = total
        self.money = 10
        self.stock = {food: self.total}

    def produce(self):
        for i in self.desires:
            self.stock[i] -= self.total

    def remove_stock(self, _1, _2):
        pass

    def add_stock(self, product, quantity):
        if product in self.stock:
            self.stock[product] += quantity
        else:
            self.stock[product] = quantity

    def get_sell_offers(self):
        # the labor offer is the average cost of the worker
        # to start with, we handle this as a fixed cost
        # 1 unit of money per worker
        return [SellOffer(self, self.labor, self.total, 1)]

    def get_buy_orders(self):
        # workers require 1 food per worker per cycle
        max_price = self.money / self.total
        return [BuyOffer(self, self.desires[0], self.total, max_price)]


class Product:
    def __init__(self, name, required=None):
        self.name = name
        if required is None:
            self.required = []
        else:
            self.required = required

    def requirement(self, total):
        return Requirement(self, total)

    def get_max_production(self, stock):
        # given these workers and the required stock, return the most that
        # can be produced
        max_production = None
        for requirement in self.required:
            if requirement.product not in stock:
                # we don't have this item
                return 0.0
            production_limit = stock[requirement.product] / requirement.total
            if max_production is None:
                max_production = production_limit
            else:
                if production_limit < max_production:
                    max_production = production_limit
        return max_production


class Producer:
    # a producer should only be able to adjust labor by a certain amount
    # let's start by having that fixed for now
    def __init__(self, product, money, stock=None):
        self.product = product
        self.money = float(money)
        if stock is None:
            self.stock = {}
        else:
            self.stock = stock
        self.stock[self.product] = 0.0
        self.last_consumption = {}

    def consume_stock(self, production):
        # this has already been checked against stock
        # remove what we needed for the last production run
        # return what was consumed
        consumed = {}
        for required in self.product.required:
            amount_used = production * required.total
            self.stock[required.product] -= amount_used
            consumed[required.product] = amount_used
        return consumed

    def remove_stock(self, product, quantity):
        if product in self.stock:
            self.stock[product] -= quantity
        else:
            raise EconomyNoStockToRemove(f'Error: No {product.name} to remove')

    def add_stock(self, product, quantity):
        if product in self.stock:
            self.stock[product] += quantity
        else:
            self.stock[product] = quantity

    def produce(self):
        # produce what we can, given our resources
        production = self.product.get_max_production(self.stock)
        self.last_consumption = self.consume_stock(production)
        self.stock[self.product] += production

    def get_sell_offers(self):
        # take all the stock we have and offer it for a price (for now, fixed)
        available_to_sell = self.stock[self.product]
        if available_to_sell == 0:
            return []
        return [SellOffer(self, self.product, available_to_sell, 1.0)]

    def get_buy_orders(self):
        # look at what we consumed and buy it back
        orders = []
        for product, total in self.last_consumption.items():
            orders.append(BuyOffer(self, product, total, 1.0))
        return orders