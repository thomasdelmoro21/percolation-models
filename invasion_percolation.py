"""
author: Thomas Del Moro

Site Percolation on 2D lattice
"""

import numpy as np
import statistics
import matplotlib.pyplot as plt
import matplotlib.patches as patches

width = 100
height = 100
eight_neighbors = False

num_runs = 5  # from 1 to infinity


def setup():
    grid = np.zeros((height, width))
    grid[0, :] = np.ones(width)
    randoms = np.random.rand(height, width)
    randoms[0, :] = np.zeros(width)
    return grid, randoms


def get_infected_nodes(grid):
    return [tuple(x) for x in np.argwhere(grid == 1)]


def get_susceptible_neighbors(grid, node):
    x, y = node[1], node[0]
    if eight_neighbors:
        neighbors = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1),
                     (y - 1, x - 1), (y + 1, x - 1), (y - 1, x + 1), (y + 1, x + 1)]
    else:
        neighbors = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]

    susceptible_neighbors = []
    for ny, nx in neighbors:
        if 0 <= ny < height and 0 <= nx < width and grid[ny, nx] == 0:
            susceptible_neighbors.append((ny, nx))
    return susceptible_neighbors


def find_min(grid, randoms, infected_nodes):
    min_value = 1
    for infected_node in infected_nodes:
        neighbors = get_susceptible_neighbors(grid, infected_node)
        for neighbor in neighbors:
            cur_value = randoms[neighbor]
            if cur_value < min_value:
                min_value = cur_value
    return min_value


def invade(grid, randoms, infection_probability, infected_nodes):
    active = True
    while active:
        new_infected = []
        for infected_node in infected_nodes:
            neighbors = get_susceptible_neighbors(grid, infected_node)
            for neighbor in neighbors:
                if randoms[neighbor] <= infection_probability and neighbor not in new_infected:
                    new_infected.append(neighbor)
        if len(new_infected) == 0:
            active = False
        else:
            for node in new_infected:
                grid[node] = 1
                infected_nodes.append(node)

    return 1 if np.sum(grid[-1, :]) > 0 else 0  # True if percolated


def simulate():
    grid, randoms = setup()
    infected_nodes = get_infected_nodes(grid)
    infectivity = 0
    percolated = False
    with plt.ion():
        fig = plt.figure()
        plt.title("p = 0")
        im = plt.imshow(grid, cmap="Blues", vmin=0, vmax=1)
        while not percolated:
            infectivity = find_min(grid, randoms, infected_nodes)
            percolated = invade(grid, randoms, infectivity, infected_nodes)

            im.set_data(grid)
            plt.title("p = {}".format(round(infectivity, 4)))
            fig.canvas.flush_events()
    plt.show(block=False)
    return infectivity


def find_threshold():
    thresholds = []
    thresholds_means = []
    for i in range(num_runs):
        plt.close()
        thresholds.append(simulate())
        thresholds_means.append(statistics.mean(thresholds))

    plt.figure()
    plt.plot(thresholds, '-o', label="Threshold")
    plt.plot(thresholds_means, '-o', label="Threshold Mean")
    plt.legend()
    plt.ylabel("Infectivity")
    plt.xlabel("N_Runs")
    plt.title("Threshold Estimate: {}".format(round(thresholds_means[-1], 4)))
    plt.show()
    print(thresholds_means[-1])


find_threshold()
