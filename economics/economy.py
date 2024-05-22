from economics.history import History
from economics.auctions import auction


class Economy:
    def __init__(self, products, producers):
        self.products = {}
        for i in products:
            self.products[i.name] = i
        self.producers = producers
        self.history = History()

    def get_all_sells(self):
        sells = []
        for producer in self.producers:
            sells.extend(producer.get_sell_offers())
        return sells

    def get_all_buys(self):
        # every worker requires some food
        # since food is essential, the maximum price to buy will be the total demand / avaliable money
        buys = []
        for producer in self.producers:
            buys.extend(producer.get_buy_orders())
        return buys

    def single_cycle(self):
        # the cycle is as follows
        # we cannot start from zero, since no such system starts like this
        # therefore each producer starts with an amount of employees, money and the like
        # because of this, we can start by producing all the goods
        # once this is done, we can get all sells and buys, and then conduct the auction
        # it may be that it is better for producers to not sell all stock to start with
        for producer in self.producers:
            producer.produce()
        buys = self.get_all_buys()
        sells = self.get_all_sells()
        auctions = auction(sells, buys)
        self.history.update(auctions)
