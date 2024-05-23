# stratagies a producer could take


def adjust_price_by_sales(producer, history):
    # this decides what price the producer sets
    # we need some basics here
    # of the things I tried to sell, what % did I sell?
    # what was the market like for this product?
    # were there unfulfilled orders in this product in the last cycle?
    producer_sales = producer.cycle_history[-1].get_sale_info(producer.product.id)
    market_sales = history.get_last_sales(producer.product.id)
    return producer.sale_price
