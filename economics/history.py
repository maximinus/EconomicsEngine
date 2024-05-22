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
    def __init__(self, max_p, min_p, avg, vol):
        self.price_range = PriceRange(min_p, max_p)
        self.average_price = avg
        self.volume = vol

    def __repr__(self):
        return f'{self.price_range}, Avg: {self.average_price:.2f}, Vol: {self.volume:.2f}'


def group_transactions_by_product(transactions):
    products_sold = {}
    for transaction in transactions:
        if transaction.product in products_sold:
            products_sold[transaction.product].append(transaction)
        else:
            products_sold[transaction.product] = [transaction]
    return products_sold


class History:
    def __init__(self):
        self.cycle_history = []

    def update(self, transactions):
        products_sold = group_transactions_by_product(transactions)
        # now calculate the history for this cycle for each listed product
        stats = {}
        for product, all_sales in products_sold.items():
            quantity_sold = 0
            total_value = 0
            max_price = 0
            min_price = math.inf
            for sale in all_sales:
                quantity_sold += sale.quantity
                total_value += sale.value
                max_price = max(max_price, sale.price)
                min_price = min(min_price, sale.price)
            stats[product] = ProductCycleStats(max_price, min_price, total_value / quantity_sold, quantity_sold)
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
