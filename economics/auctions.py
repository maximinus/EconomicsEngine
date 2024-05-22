from economics.offers import Transaction


class SingleAuction:
    def __init__(self):
        self.sells = []
        self.buys = []
        self.transactions = []

    @property
    def valid(self):
        # are there at least >1 buy and sell offers?
        if len(self.sells) == 0:
            return False
        if len(self.buys) == 0:
            return False
        return True

    def do_transaction(self, sell, buy):
        # buyer will buy as many as they can at this price
        # The unit cost of the product is equal to the (sell cost + buy price) / 2.0
        quantity_sold = max(buy.total_wanted, sell.total_offered)
        unit_cost = (sell.cost_per_unit + buy.max_price) / 2.0
        total_cost = unit_cost * quantity_sold
        sell.seller.money += total_cost
        buy.buyer.money -= total_cost
        buy.buyer.add_stock(buy.product, quantity_sold)
        sell.seller.remove_stock(buy.product, quantity_sold)
        sell.total_offered -= quantity_sold
        buy.total_wanted -= quantity_sold
        self.transactions.append(Transaction(buy.product, quantity_sold, unit_cost))

    def perform(self):
        if not self.valid:
            return
        # sort buys by highest bid and sells by lowest ask
        self.sells = sorted(self.sells, key=lambda offer: offer.cost_per_unit)
        self.buys = sorted(self.buys, key=lambda buy: buy.max_price)
        self.buys.reverse()
        # continue until no more buys or sells for this product
        while len(self.buys) > 0 and len(self.sells) > 0:
            if self.buys[0].max_price >= self.sells[0].cost_per_unit:
                self.do_transaction(self.sells[0], self.buys[0])
            else:
                # max price offered is lower than the smallest ask price; we stop here
                return self.transactions
            # check if the current buy or sell is done
            if self.sells[0].total_offered == 0:
                self.sells.pop(0)
            if self.buys[0].total_wanted == 0:
                self.buys.pop(0)
        return self.transactions


def create_auctions(sells, buys):
    # organise an auction to match sellers with buyers
    # the auction is separate for each different type of product, so first match these
    auctions = {}
    for sell_order in sells:
        if sell_order.product in auctions:
            auctions[sell_order.product].sells.append(sell_order)
        else:
            new_auction = SingleAuction()
            new_auction.sells.append(sell_order)
            auctions[sell_order.product] = new_auction
    # now add the buys
    for buy_order in buys:
        if buy_order.product in auctions:
            auctions[buy_order.product].buys.append(buy_order)
        else:
            new_auction = SingleAuction()
            new_auction.buys.append(buy_order)
            auctions[buy_order.product] = new_auction
    return auctions


def auction(sells, buys):
    auctions = create_auctions(sells, buys)
    all_transactions = []
    for _, single_auction in auctions.items():
        all_transactions.extend(single_auction.perform())
    return all_transactions
