"""
@author Thomas Del Moro
"""

import random
import numpy as np


class Lattice:
    def __init__(self, width, height, eight_neighbors):
        self.height = height
        self.width = width
        self.grid = np.zeros((height, width))
        self.randoms = np.random.rand(height, width)
        self.infection_time = np.zeros((height, width))
        self.eight_neighbors = eight_neighbors

    def reset(self):
        self.grid = np.zeros((self.height, self.width))
        self.randoms = np.random.rand(self.height, self.width)

    def infect_node(self, node):
        self.grid[node] = 1
        self.randoms[node] = random.random()

    def infect_nodes(self, nodes):
        for node in nodes:
            self.grid[node] = 1
            self.randoms[node] = random.random()

    def recover_node(self, node):
        self.grid[node] = 2
        self.randoms[node] = random.random()

    def is_susceptible(self, node):
        return True if self.grid[node] == 0 else False

    def get_infected_nodes(self):
        return [tuple(x) for x in np.argwhere(self.grid == 1)]

    def get_data(self):
        susceptible_fraction = np.count_nonzero(self.grid == 0) / (self.width * self.height)
        infected_fraction = np.count_nonzero(self.grid == 1) / (self.width * self.height)
        recovered_fraction = np.count_nonzero(self.grid == 2) / (self.width * self.height)
        return [susceptible_fraction, infected_fraction, recovered_fraction]

    def get_susceptible_neighbors(self, node):
        x, y = node[1], node[0]
        if self.eight_neighbors:
            neighbors = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1),
                         (y - 1, x - 1), (y + 1, x - 1), (y - 1, x + 1), (y + 1, x + 1)]
        else:
            neighbors = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]

        susceptible_neighbors = []
        for ny, nx in neighbors:
            if 0 <= ny < self.height and 0 <= nx < self.width and self.is_susceptible((ny, nx)):
                susceptible_neighbors.append((ny, nx))
        return susceptible_neighbors
