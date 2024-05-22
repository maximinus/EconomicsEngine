import math
import statistics
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


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


class History:
    def __init__(self):
        self.cycle_history = []

    def update(self, auctions):
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
            avg = total_value / quantity_sold
            s = ProductCycleStats(max_price, min_price, avg, quantity_sold, auction.unsold, auction.unfilled_orders)
            stats[auction.product] = s
        self.cycle_history.append(stats)

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


def show_average_price_graph(history):
    # we need to calculate the entirety of prices
    # some years may be missing a price, for this we need to save "zero"
    # get all listed products first
    averages = {}
    for i in history.cycle_history:
        for product in i.keys():
            if product not in averages:
                averages[product] = []
    for i in history.cycle_history:
        # examine every product sold over this cycle
        for product in i.keys():
            if product in i:
                averages[product].append(i[product].average_price)
            else:
                # this cycle has no volume for this product
                averages[product].append(0)

    # now we can generate the graph
    # we have a dict of {product: array_of_average_prices}
    fig, ax = plt.subplots()
    for product, values in averages.items():
        ax.plot(values, label=product.name)
    ax.legend()
    ax.set_xlabel('Cycle')
    ax.set_ylabel('Price')
    ax.set_title('Average Prices')
    plt.show()
