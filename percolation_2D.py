"""
author: Thomas Del Moro

Site Percolation on 2D lattice
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

width = 100
height = 100
eight_neighbors = False

infectivity = 0.5  # only if you run one simulation
num_runs = 10  # number of runs per infection probability, only if you compute threshold


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


def invade(grid, randoms, infection_probability, plt_block):
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
                    if randoms[neighbor] < infection_probability and neighbor not in new_infected:
                        new_infected.append(neighbor)
            if len(new_infected) == 0:
                active = False
            else:
                for node in new_infected:
                    grid[node] = 1
                    infected_nodes.append(node)

            im.set_data(grid)
            fig.canvas.flush_events()

    plt.show() if plt_block else plt.close()
    return 1 if np.sum(grid[-1, :]) > 0 else 0  # True if percolated


def simulate(infection_probability, plt_block=True):
    grid, randoms = setup()
    return invade(grid, randoms, infection_probability, plt_block)


def find_threshold():
    infectivities = np.linspace(0.55, 0.65, 40)
    threshold_data = []
    for infection_probability in infectivities:
        tot_percolations = 0
        for i in range(num_runs):
            percolated = simulate(infection_probability, plt_block=False)
            if percolated:
                tot_percolations += 1
        threshold_data.append(tot_percolations / num_runs)

    fig, ax = plt.subplots()
    ax.plot(infectivities, threshold_data, 'o', color="red")
    rect = patches.Rectangle((0.5827, 0.), 0.02, 1.0, linewidth=0.8, edgecolor="#dddddd", facecolor="None")
    ax.add_patch(rect)
    plt.show()


# simulate(infectivity)
find_threshold()
