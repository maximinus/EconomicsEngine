class SellOffer:
    def __init__(self, seller, product_id, total, cost_per_unit):
        self.seller = seller
        self.product_id = product_id
        self.total_offered = float(total)
        self.cost_per_unit = float(cost_per_unit)

    def copy(self):
        return SellOffer(self.seller, self.product_id, self.total_offered, self.cost_per_unit)

    @property
    def value(self):
        return self.total_offered * self.cost_per_unit

    def __repr__(self):
        return f'Sell {self.total_offered} {self.product_id} @ {self.cost_per_unit} each'


class BuyOffer:
    # a buy offer has a maximum price, i.e. the most that will be paid
    def __init__(self, buyer, product_id, total, max_price):
        self.buyer = buyer
        self.product_id = product_id
        self.total_wanted = float(total)
        self.max_price = float(max_price)

    def copy(self):
        return BuyOffer(self.buyer, self.product_id, self.total_wanted, self.max_price)

    def __repr__(self):
        return f'Buy up to {self.total_wanted} {self.product_id} @ max {self.max_price} each'


class Transaction:
    def __init__(self, product_id, quantity, price):
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    @property
    def value(self):
        return self.quantity * self.price

    def __repr__(self):
        return f'{self.quantity} x {self.product_id} @ {self.price}'
