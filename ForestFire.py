"""
author: Thomas Del Moro

Forest Fire

Empty: 0
Susceptible Tree: 1
Burned Tree: 2
"""

import random
import matplotlib.pyplot as plt
import numpy as np

width = 200
height = 200
eight_neighbors = False
density = 0.6
init_burned = 1
num_simulations = 5
seed = None


def setup(num_burned=1):
    grid = np.zeros((height, width))
    num_trees = int(density * width * height)
    burned_indices = np.random.choice(range(width * height), size=num_trees, replace=False)
    grid[np.unravel_index(burned_indices, (height, width))] = 1

    return grid, infect_random(grid, num_burned)


def infect_random(grid, num_burned):
    burned = []
    while len(burned) < num_burned:
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        if grid[y, x] == 1:
            grid[y, x] = 2
            burned.append((y, x))
    return burned


def get_susceptible_neighbors(grid, node):
    x, y = node[1], node[0]
    if eight_neighbors:
        neighbors = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1),
                     (y - 1, x - 1), (y + 1, x - 1), (y - 1, x + 1), (y + 1, x + 1)]
    else:
        neighbors = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]

    susceptible_neighbors = []
    for ny, nx in neighbors:
        if 0 <= ny < height and 0 <= nx < width and grid[ny, nx] == 1:
            susceptible_neighbors.append((ny, nx))
    return susceptible_neighbors


def step(grid, burned_trees):
    new_burned = []
    for tree in burned_trees:
        neighbors = get_susceptible_neighbors(grid, tree)
        for neighbor in neighbors:
            grid[neighbor] = 2
            new_burned.append(neighbor)
    return new_burned


def simulate():
    active = True
    grid, burned_trees = setup(init_burned)
    burned_data = []
    with plt.ion():
        fig = plt.figure()
        im = plt.imshow(grid, cmap="summer", vmin=0, vmax=2)
        while active:
            new_burned = step(grid, burned_trees)
            if len(new_burned) > 0:
                for tree in new_burned:
                    burned_trees.append(tree)
                burned_data.append(len(burned_trees))
            else:
                active = False

            im.set_data(grid)
            fig.canvas.flush_events()
    print(grid)
    return burned_data


def plot_single_simulation(burned_data):
    plt.figure()
    plt.plot(burned_data, '-o', lw=1)
    plt.xlabel("Time")
    plt.ylabel("Number of Burned Trees")
    plt.title("Forest Fire Simulation")
    plt.show()


def simulate_multiple():
    pass


burned_data = simulate()
plot_results(burned_data)
