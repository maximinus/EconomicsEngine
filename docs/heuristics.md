# Producer Intelligence

## Overview

Producers need some intelligence to accurately work with the market. This we do with a series of heuristics. Not every producer has the same heuristics.


### Basic Heuristics

Although most of our rules may be about pricing, it may be good to consider some overall guidelines. For example:

* Place some limit on spending per turn
* Try to keep a certain minimum level of stock
* Do not sell all produce every turn


### Determining Price

To determine price, the producer must try to maximise the sell price and minimise the buy price.

Therefore, they may try to:

* Buy required stock when prices in that are low
* Sell product when the price rises
* Not sell product when prices are too low

Things that a producer can check:

* The historical price of a stock
* The recent cycle highs and lows of a stock
* The volume of trades of a particular stock
* Whether all offered products were sold
* Whether all offered buys were obtained


A producer should always aim to make a profit, but there are different ways of calculating if you make a profit

You could take the total unit cost of the stock you have now and use that as the base price.
You could take the unit cost of the stock if you bought in the last cycle, or the average of some previous cycles
If both of these methods are significantly below the current market price, you could base it on the average selling cost of the product.
