"""
@author Thomas Del Moro
"""

import numpy as np


class Lattice:
    def __init__(self, width, height, eight_neighbors):
        self.height = height
        self.width = width
        self.grid = np.zeros((height, width))
        self.randoms = np.random.rand(height, width)
        self.eight_neighbors = eight_neighbors

    def infect_node(self, node):
        self.grid[node] = 1
        self.randoms[node] = 0

    def infect_nodes(self, nodes):
        for node in nodes:
            self.grid[node] = 1
            self.randoms[node] = 0

    def is_infected(self, node):
        return True if self.grid[node] == 1 else False

    def get_infected_nodes(self):
        return np.argwhere(self.grid == 1)

    def get_infected_fraction(self):
        return np.count_nonzero(self.grid == 1) / (self.width * self.height)

    def get_susceptible_neighbors(self, node):
        neighbors = []
        x, y = node[1], node[0]
        if y > 0 and not self.is_infected((y - 1, y)):
            neighbors.append((y - 1, x))
        if y < self.height - 1 and not self.is_infected((y + 1, x)):
            neighbors.append((y + 1, x))
        if x > 0 and not self.is_infected((y, x - 1)):
            neighbors.append((y, x - 1))
        if x < self.width - 1 and not self.is_infected((y, x + 1)):
            neighbors.append((y, x + 1))

        if self.eight_neighbors:
            if y > 0 and x > 0 and not self.is_infected((y - 1, x - 1)):
                neighbors.append((y - 1, x - 1))
            if y < self.height - 1 and x > 0 and not self.is_infected((y + 1, x - 1)):
                neighbors.append((y + 1, x - 1))
            if y > 0 and x < self.width - 1 and not self.is_infected((y - 1, x + 1)):
                neighbors.append((y - 1, x + 1))
            if y < self.height - 1 and x < self.width - 1 and not self.is_infected((y + 1, x + 1)):
                neighbors.append((y + 1, x + 1))

        return neighbors
