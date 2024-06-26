"""
author: Thomas Del Moro

SIS model
S (Susceptible): 0
I (Infected): 1
S (Susceptible): 0
"""

import random
import matplotlib.pyplot as plt
import numpy as np


width = 100
height = 100
eight_neighbors = True
infection_rate = 0.4
recover_rate = 0.5  # 1 / days_to_recover
num_infected = 1
num_simulations = 1
termination_time = 1000
seed = None


def infect_random():
    if seed is not None:
        random.seed(seed)
    infected_nodes = [(random.randint(0, height - 1), random.randint(0, width - 1)) for _ in range(num_infected)]
    for node in infected_nodes:
        grid[node] = 1


def get_infected_nodes():
    return [tuple(x) for x in np.argwhere(grid == 1)]


def get_susceptible_neighbors(node):
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


def step():
    infected_nodes = get_infected_nodes()
    new_infected = []
    for infected_node in infected_nodes:
        # INFECT NEIGHBORS
        neighbors = get_susceptible_neighbors(infected_node)
        for neighbor in neighbors:
            if infection_rate > random.random() and neighbor not in new_infected:
                new_infected.append(neighbor)
        # RECOVER
        if random.random() < recover_rate:
            grid[infected_node] = 0

    for node in new_infected:
        grid[node] = 1


def simulate_SIS():
    infect_random()
    active = True
    susceptible_data = []
    infected_data = []
    with plt.ion():
        fig = plt.figure()
        im = plt.imshow(grid, cmap="viridis", vmin=0, vmax=1)
        while active:
            step()
            susceptible_data.append(np.count_nonzero(grid == 0) / (width * height))
            infected_data.append(np.count_nonzero(grid == 1) / (width * height))
            if susceptible_data[-1] == 1 or infected_data[-1] == 1 or len(susceptible_data) > termination_time:
                active = False
            im.set_data(grid)
            fig.canvas.flush_events()
            plt.pause(0.1)
    print(grid)
    return susceptible_data, infected_data


def simulate_multiple_SIS():
    susceptible_data = []
    infected_data = []
    for sim in range(num_simulations):
        grid[:, :] = 0
        susceptible_sim, infected_sim = simulate_SIS()
        plt.close()
        susceptible_data.append(susceptible_sim)
        infected_data.append(infected_sim)
    min_len = min([len(x) for x in susceptible_data])
    susceptible_data = np.array([x[:min_len] for x in susceptible_data])
    infected_data = np.array([x[:min_len] for x in infected_data])
    susceptible_data = np.mean(susceptible_data, axis=0)
    infected_data = np.mean(infected_data, axis=0)
    plot_simulation(susceptible_data, infected_data)


def plot_simulation(susceptible_data, infected_data):
    fig, ax = plt.subplots()
    ax.plot(susceptible_data, 'b', alpha=0.5, lw=2, label="Susceptible")
    ax.plot(infected_data, 'r', alpha=0.5, lw=2, label="Infected")
    ax.set_xlabel("Time")
    ax.set_ylabel("Fraction of Population")
    ax.set_title("SIS")
    ax.legend()
    plt.show()


grid = np.zeros((height, width))
simulate_SIS()

