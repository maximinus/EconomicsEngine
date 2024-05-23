# stratagies a producer could take


def adjust_price_by_sales(producer, history):
    # this decides what price the producer sets
    # we need some basics here
    # what % of the sell orders were sold last time?
    # what % of all product sell orders were sold last time?
    # what % of buy orders were not fulfilled the last time?
    # the history is only going to tell me what the market was like, I also need to know
    # what it was like for me
    sales = history.get_last_sales(producer.product.id)
    return producer.sale_price
