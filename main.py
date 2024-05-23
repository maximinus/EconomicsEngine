from pathlib import Path

from economics.loader import load_economy
from economics.history import show_average_price_graph

CONFIG_FILE = Path('./examples/basic.json')


if __name__ == '__main__':
    economy = load_economy(CONFIG_FILE)
    for i in range(4):
        economy.single_cycle()
    show_average_price_graph(economy)
