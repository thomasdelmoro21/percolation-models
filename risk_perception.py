"""
author: Thomas Del Moro

Site Percolation on 2D lattice
"""
import math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

width = 100
height = 100
eight_neighbors = True

risk_perception_factor = 0.5  # only if you run one simulation
infectivity = 0.5  # only if you run one simulation
max_factor = 10  # number of runs per infection probability, only if you compute threshold


def setup():
    grid = np.zeros((height, width))
    grid[0, :] = np.ones(width)
    randoms = np.random.rand(height, width)
    randoms[0, :] = np.zeros(width)
    return grid, randoms


def get_infected_nodes(grid):
    return [tuple(x) for x in np.argwhere(grid == 1)]


def get_neighbors(node):
    x, y = node[1], node[0]
    if eight_neighbors:
        neighs = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1),
                  (y - 1, x - 1), (y + 1, x - 1), (y - 1, x + 1), (y + 1, x + 1)]
    else:
        neighs = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]

    neighbors = []
    for ny, nx in neighs:
        if 0 <= ny < height and 0 <= nx < width:
            neighbors.append((ny, nx))
    return neighbors


def get_susceptible_neighbors(grid, node):
    neighbors = get_neighbors(node)
    susceptible_neighbors = []
    for neighbor in neighbors:
        if grid[neighbor] == 0:
            susceptible_neighbors.append(neighbor)
    return susceptible_neighbors


def get_infected_neighbors(grid, node):
    neighbors = get_neighbors(node)
    infected_neighbors = []
    for neighbor in neighbors:
        if grid[neighbor] == 1:
            infected_neighbors.append(neighbor)
    return infected_neighbors


def invade(grid, randoms, infection_probability, risk_perception, plt_block):
    infected_nodes = [(0, x) for x in range(width)]
    active = True
    with plt.ion():
        fig = plt.figure()
        plt.title("Infectivity = {}".format(round(infection_probability, 3)))
        im = plt.imshow(grid, cmap="Reds", vmin=0, vmax=1)
        while active:
            new_infected = []
            for infected_node in infected_nodes:
                # INFECT NEIGHBORS
                neighbors = get_susceptible_neighbors(grid, infected_node)
                for neighbor in neighbors:
                    num_neighs = len(get_neighbors(neighbor))
                    num_inf_neighs = len(get_infected_neighbors(grid, neighbor))
                    if randoms[neighbor] < infection_probability * math.exp(-1 * risk_perception * num_inf_neighs / num_neighs) and neighbor not in new_infected:
                        new_infected.append(neighbor)
            if len(new_infected) == 0 or sum(grid[-1, :]) > 0:
                active = False
            else:
                for node in new_infected:
                    grid[node] = 1
                    infected_nodes.append(node)

            im.set_data(grid)
            fig.canvas.flush_events()

    plt.show() if plt_block else plt.close()
    return 1 if np.sum(grid[-1, :]) > 0 else 0  # True if percolated


def simulate(tau, j, plt_block=True):
    grid, randoms = setup()
    return invade(grid, randoms, tau, j, plt_block)


def find_threshold():
    infectivities = np.linspace(0.2, 0.8, 20)
    risk_perceptions = [i/10 for i in range(0, max_factor*10)]
    threshold_data = dict()
    for tau in infectivities:
        for j in risk_perceptions:
            percolated = simulate(tau, j, plt_block=False)
            print(tau, j, percolated)
            if not percolated:
                threshold_data[tau] = j
                break

    fig, ax = plt.subplots()
    ax.plot(threshold_data.keys(), threshold_data.values(), 'o', color="red")
    print(threshold_data)
    plt.show()


find_threshold()