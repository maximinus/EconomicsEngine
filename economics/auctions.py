from economics.offers import Transaction
from economics.producer import BuyResult, SellResult


class SingleAuction:
    def __init__(self, product_id):
        self.product_id = product_id
        self.sells = []
        self.buys = []
        self.transactions = []
        # keep a list of goods that were not sold, and orders unfilled
        self.unsold = 0
        self.unfilled_orders = 0

    @property
    def valid(self):
        # are there at least >1 buy and sell offers?
        return not (len(self.sells) == 0 or len(self.buys) == 0)

    def do_transaction(self, sell, buy):
        # buyer will buy as many as they can at this price
        # The unit cost of the product is equal to the (sell cost + buy price) / 2.0
        quantity_sold = max(buy.total_wanted, sell.total_offered)
        unit_cost = (sell.cost_per_unit + buy.max_price) / 2.0
        total_cost = unit_cost * quantity_sold
        sell.seller.money += total_cost
        buy.buyer.money -= total_cost
        buy.buyer.add_stock(buy.product_id, quantity_sold)
        sell.seller.remove_stock(buy.product_id, quantity_sold)
        sell.total_offered -= quantity_sold
        buy.total_wanted -= quantity_sold
        # the 2 producers here will need some signals about their sales
        sell.seller.add_sale(SellResult(sell.cost_per_unit, unit_cost, quantity_sold, buy.product_id))
        buy.buyer.add_purchase(BuyResult(buy.max_price, unit_cost, quantity_sold, buy.product_id))
        self.transactions.append(Transaction(buy.product_id, quantity_sold, unit_cost))

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
                # this means that there is at least ONE order that was unfulfilled
                break
            # check if the current buy or sell is done
            if self.sells[0].total_offered == 0:
                self.sells.pop(0)
            if self.buys[0].total_wanted == 0:
                self.buys.pop(0)
        # calculate unfilled and unsold orders by volume
        self.unsold = sum([x.total_wanted for x in self.buys])
        self.unfilled_orders = sum([x.total_offered for x in self.sells])


def create_auctions(sells, buys):
    # organise an auction to match sellers with buyers
    # the auction is separate for each different type of product, so first match these
    auctions = {}
    for sell_order in sells:
        if sell_order.product_id in auctions:
            auctions[sell_order.product_id].sells.append(sell_order)
        else:
            new_auction = SingleAuction(sell_order.product_id)
            new_auction.sells.append(sell_order)
            auctions[sell_order.product_id] = new_auction
    # now add the buys
    for buy_order in buys:
        if buy_order.product_id in auctions:
            auctions[buy_order.product_id].buys.append(buy_order)
        else:
            new_auction = SingleAuction(buy_order.product_id)
            new_auction.buys.append(buy_order)
            auctions[buy_order.product_id] = new_auction
    return auctions


def auction(sells, buys):
    auctions = create_auctions(sells, buys)
    all_auctions = []
    for _, single_auction in auctions.items():
        single_auction.perform()
        all_auctions.append(single_auction)
    return all_auctions
