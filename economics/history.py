import math
import statistics
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


# take a step back
# we need to store a historical record for 2 reasons:
# we want to show the data
# we want entities to be able to reason about the past
# the simulation depends on cycles, so we save an array of cycle information
# the cycle information we want is:
# for every product, the quantity traded, the max and min prices, the amount unsold and offers unfilled
# for every producer, starting stock and money
# we convert the stock from a dict to a simple list of lists, which means giving every product an ID
# also producers need an ID for the same reason.

# we capture the producer info at the start of the process, and the trade infor after the auction


class PriceRange:
    def __init__(self, min_price, max_price):
        self.min_price = float(min_price)
        self.max_price = float(max_price)

    @property
    def valid(self):
        return self.min_price < 0.0

    def __repr__(self):
        return f'Price: {self.min_price:.2f}->{self.max_price:.2f}'


class ProductCycleStats:
    # represents what happened to a product in a given cycle
    def __init__(self, max_p, min_p, avg, vol, unsold, unfilled):
        self.price_range = PriceRange(min_p, max_p)
        self.average_price = avg
        self.volume = vol
        self.unsold = 0
        self.unfilled_orders = 0

    def __repr__(self):
        return f'{self.price_range}, Avg: {self.average_price:.2f}, Vol: {self.volume:.2f}'


def convert_producer_stock(producer):
    # convert the producer stock to something simpler
    pass


class CycleInfo:
    def __init__(self, trades, goods):
        # this is a dict of {product_id:ProductCycleStats}
        self.trades_info = trades
        # this is a dict of {producer_id:[money, [product:amount]}
        self.goods = goods


class History:
    def __init__(self):
        self.cycle_history = []
        self.producers_this_cycle = None

    def create_sales_stats(self, auctions):
        transactions = []
        [transactions.extend(x.transactions) for x in auctions]
        # now calculate the history for this cycle for each listed product
        stats = {}
        for auction in auctions:
            quantity_sold = 0
            total_value = 0
            max_price = 0
            min_price = math.inf
            for sale in auction.transactions:
                quantity_sold += sale.quantity
                total_value += sale.value
                max_price = max(max_price, sale.price)
                min_price = min(min_price, sale.price)
            if quantity_sold > 0:
                avg = total_value / quantity_sold
            else:
                avg = 0.0
            s = ProductCycleStats(max_price, min_price, avg, quantity_sold, auction.unsold, auction.unfilled_orders)
            stats[auction.product_id] = s
        return stats

    def update_producers(self, producers):
        self.producers_this_cycle = [convert_producer_stock(x) for x in producers]

    def update_auctions(self, auctions):
        stats = self.create_sales_stats(auctions)
        assert self.producers_this_cycle is not None
        self.cycle_history.append(CycleInfo(stats, self.producers_this_cycle))
        self.producers_this_cycle = None

    def get_last_price(self, product):
        last_cycle = self.cycle_history[-1]
        if product not in last_cycle:
            return -1
        return last_cycle[product].average_price

    def get_last_volume(self, product):
        last_cycle = self.cycle_history[-1]
        if product not in last_cycle:
            return -1
        return last_cycle[product].volume

    def get_last_price_range(self, product):
        last_cycle = self.cycle_history[-1]
        if product not in last_cycle:
            return PriceRange(-1, -1)
        return last_cycle[product].price_range

    def get_last_unsold(self, product):
        last_cycle = self.cycle_history[-1]
        if product not in last_cycle:
            return 0
        return last_cycle.unsold

    def get_last_unfilled(self, product):
        last_cycle = self.cycle_history[-1]
        if product not in last_cycle:
            return 0
        return last_cycle.unfilled_orders

    def get_product_history(self, product, cycles):
        cycles = min(cycles, len(self.cycle_history))
        return [self.cycle_history[x].get(product, None) for x in range(-cycles, 0)]

    def get_long_term_price(self, product, cycles):
        stats = self.get_product_history(product, cycles)
        prices = [x.average_price for x in stats if x is not None]
        if len(prices) == 0:
            return -1
        return statistics.mean(prices)

    def get_long_term_volume(self, product, cycles):
        stats = self.get_product_history(product, cycles)
        prices = [x.volume for x in stats if x is not None]
        if len(prices) == 0:
            return -1
        return statistics.mean(prices)


def show_average_price_graph(economy):
    # we need to calculate the entirety of prices
    # some years may be missing a price, for this we need to save "zero"
    # get all listed products first
    history = economy.history
    averages = {}
    for i in history.cycle_history:
        for product in i.trades_info.keys():
            if product not in averages:
                averages[product] = []
    for i in history.cycle_history:
        # examine every product sold over this cycle
        for product in i.trades_info.keys():
            if product in i.trades_info:
                averages[product].append(i.trades_info[product].average_price)
            else:
                # this cycle has no volume for this product
                averages[product].append(0)

    # now we can generate the graph
    # we have a dict of {product: array_of_average_prices}
    fig, ax = plt.subplots()
    for product_id, values in averages.items():
        ax.plot(values, label=economy.get_product(product_id).name)
    ax.legend()
    ax.set_xlabel('Cycle')
    ax.set_ylabel('Price')
    ax.set_title('Average Prices')
    plt.show()
