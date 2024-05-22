# Economy v0.1


## Overview

The goal of the project is to produce a library to simulate a model economy for a game or for simple experimentation.

There are some assumptions made about how an economy works; the basics are built around a free market system with companies and competition, into which we add financial systems, workers, a government and money.

It is not the intention of the author to adhere to a particular economic or political creed; the intention is to simulate an economy.


## Basic Elements

As of the current version, there are 4 elements to an economy.

### 1: Products

A *product* is something made. Products may be produced, consumed, or naturally wear out over time.

Products may have *requirements*, which means a number of other products must be consumed to produce it. For example, if we want to make a product "Chair" we may need to consume a certain quantity of the products "Wood" and "Cloth".

*What* the product actually represents is of little importance to the simulation.


### 2: Producers

A *producer* is an entity who produce a single product. To do this, they may need to obtain other products to facilitate production. The aim of the producer is to maximise the amount of money they have, by selling the product for more than the money they spend producing it.


### 3: Workers

*Workers* represent the workforce of the economy. They are a producer who automatically "produce" labor, which is sold on the open market like another resource. Almost all products require some amount of labor.


### 4: Money

Money is used as a medium of exchange. Producers and workers hold stores of money.


## Basic Cycle

The economy progresses in cycles. Over every cycle, the following happens:

* All producers make their product
* All producers then make offers to sell their product
* The producers also make offers to buy other products
* An auction is then held to match sellers with buyers, and money and products are exchanged


### Auctions

In an auction, the following actions are performed:

* The sells and buys are sorted per product
* The sell offers are sorted from lowest value to highest value
* The buy offers are sorted from highest value to lowest value
* The buy orders are then iterated through, and are fulfilled by the sell orders
* The final cost of a product is the sale_price + buy_price / 2

An example to explain. In the market there are 4 "buy" offers and 3 "sell" offers for a product. Each of these has a price and a quantity. For the sells, this is the lowest acceptable price, and for the buys it is the highest acceptable price.
Let us assume the buy offers are as follows, ordered by highest price:

Buy: 3 products at price 10
Buy: 4 products at price 7
Buy: 2 products at price 6
Buy: 7 products at price 4

And the sell offers, ordered from cheapest to most expensive:

Sell: 6 products at price 4
Sell: 2 products at price 5
Sell: 8 products at price 6

The first "buy" is fulfilled by the first "sell", and the cost is 10 + 4 / 2 = 7
The second "buy" is fulfilled by 3 products at price (4+7)/2=5.5 and 1 product at price (5+7)/2=6
The third "buy" will buy 1 product at price (5+6)/2=5.5 and 1 product at price (6+6)/2=6
The last "buy" will not be resolved since the offer price is below the sell price.

The result of this is that 9 products will have been sold:

    * 3 @ price 7
    * 3 @ price 5.5
    * 1 @ price 6
    * 1 @ price 5.5
    * 1 @ price 6

So the quantity of goods is 9 and the value of the goods is 21+16.5+6+5.5+6 = 55, giving an average price of 6.11.

This average price is stored in a market history and producers can make decisions on future purchases based on this.
