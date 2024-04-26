"""
author: Thomas Del Moro

SIR model
S (Susceptible): 0
I (Infected): 1
R (Recovered): 2
"""

import random
import matplotlib.pyplot as plt
import numpy as np

width = 200
height = 200
eight_neighbors = True
infection_rate = 0.8
recover_rate = 0.1  # 1 / days_to_recover
num_infected = 10
num_simulations = 1
seed = 110


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


def step(infectivity, recovery):
    infected_nodes = get_infected_nodes()
    new_infected = []
    for infected_node in infected_nodes:
        # INFECT NEIGHBORS
        neighbors = get_susceptible_neighbors(infected_node)
        for neighbor in neighbors:
            if infectivity > random.random() and neighbor not in new_infected:
                new_infected.append(neighbor)
        # RECOVER
        if random.random() < recovery:
            grid[infected_node] = 2

    for node in new_infected:
        grid[node] = 1


def simulate_SIR(infectivity, recovery):
    infect_random()
    active = True
    susceptible_data = []
    infected_data = []
    recovered_data = []
    count_to_stop = 0
    with plt.ion():
        fig = plt.figure()
        plt.title("SIR p={}".format(round(infectivity, 2)))
        im = plt.imshow(grid, cmap="viridis", vmin=0, vmax=2)
        while active:
            step(infectivity, recovery)
            susceptible_data.append(np.count_nonzero(grid == 0) / (width * height))
            infected_data.append(np.count_nonzero(grid == 1) / (width * height))
            recovered_data.append(np.count_nonzero(grid == 2) / (width * height))
            if recovered_data[-1] == 1:
                active = False
            if len(recovered_data) > 2:
                count_to_stop = count_to_stop + 1 if recovered_data[-1] == recovered_data[-2] else 0
                if count_to_stop > 5:
                    active = False
            im.set_data(grid)
            fig.canvas.flush_events()
            plt.pause(0.1)
    print(grid)
    return susceptible_data, infected_data, recovered_data


def simulate_multiple_SIR():
    susceptible_data = []
    infected_data = []
    recovered_data = []
    for sim in range(num_simulations):
        grid[:, :] = 0
        susceptible_sim, infected_sim, recovered_sim = simulate_SIR(infection_rate, recover_rate)
        plt.close()
        susceptible_data.append(susceptible_sim)
        infected_data.append(infected_sim)
        recovered_data.append(recovered_sim)
    min_len = min([len(x) for x in susceptible_data])
    susceptible_data = np.array([x[:min_len] for x in susceptible_data])
    infected_data = np.array([x[:min_len] for x in infected_data])
    recovered_data = np.array([x[:min_len] for x in recovered_data])
    susceptible_data = np.mean(susceptible_data, axis=0)
    infected_data = np.mean(infected_data, axis=0)
    recovered_data = np.mean(recovered_data, axis=0)
    plot_simulation(susceptible_data, infected_data, recovered_data)
    print(tuple(recovered_data))


def plot_simulation(susceptible_data, infected_data, recovered_data):
    fig, ax = plt.subplots()
    ax.plot(susceptible_data, 'b', alpha=0.5, lw=2, label="Susceptible")
    ax.plot(infected_data, 'r', alpha=0.5, lw=2, label="Infected")
    ax.plot(recovered_data, 'g', alpha=0.5, lw=2, label="Recovered")
    ax.set_xlabel("Time")
    ax.set_ylabel("Fraction of Population")
    ax.set_title("SIR")
    ax.legend()
    plt.show()


def simulate_infectivities():
    infectivities = [0.4, 0.5, 0.6, 0.7]
    results = []
    for infectivity in infectivities:
        inf_data = []
        for sim in range(3):
            grid[:, :] = 0
            _, _, recovered_sim = simulate_SIR(infectivity, recover_rate)
            plt.close()
            inf_data.append(recovered_sim)
        results.append(inf_data)

    colors = ["r", "g", "b", "y"]
    plt.figure()
    for i in range(len(infectivities)):
        for j in range(3):
            plt.plot(results[i][j], 'x', markersize=3.0, color=colors[i], label="Infectivity = {}".format(infectivities[i])
            if j == 0 else "_nolegend_")
    plt.legend()
    plt.xlabel("Time")
    plt.ylabel("Fraction of Population")
    plt.title("SIR")
    plt.show()


def plot_neighbors():
    plt.figure()
    plt.plot([0.0, 0.0001, 0.00035, 0.000925, 0.001975, 0.002775, 0.004375, 0.006675, 0.0091, 0.012275, 0.016425, 0.02135, 0.027275, 0.0325, 0.0386, 0.0454, 0.052975, 0.0606, 0.068675, 0.07905, 0.088525, 0.099725, 0.110125, 0.121975, 0.13515, 0.14735, 0.159875, 0.1731, 0.18675, 0.199875, 0.214775, 0.228725, 0.242775, 0.25745, 0.2724, 0.2875, 0.302525, 0.317425, 0.332025, 0.346425, 0.361, 0.375475, 0.389275, 0.402725, 0.416625, 0.430975, 0.443925, 0.45695, 0.4703, 0.483475, 0.4955, 0.50835, 0.520975, 0.53345, 0.54615, 0.559675, 0.572825, 0.585425, 0.59925, 0.61215, 0.625125, 0.637725, 0.650475, 0.662775, 0.6755, 0.689575, 0.70205, 0.714375, 0.725975, 0.7382, 0.74955, 0.760875, 0.772, 0.78215, 0.792175, 0.80185, 0.810825, 0.81965, 0.828175, 0.836575, 0.843725, 0.85185, 0.858475, 0.86485, 0.87135, 0.8778, 0.883475, 0.8886, 0.893975, 0.898975, 0.903625, 0.908025, 0.912225, 0.916475, 0.91985, 0.92355, 0.92685, 0.930075, 0.933375, 0.93685, 0.940325, 0.943375, 0.946025, 0.948825, 0.951525, 0.953975, 0.9566, 0.9595, 0.961425, 0.963325, 0.9655, 0.967525, 0.96915, 0.970875, 0.9729, 0.9746, 0.975875, 0.97735, 0.979075, 0.980675, 0.9819, 0.98325, 0.984225, 0.9857, 0.9871, 0.98805, 0.9888, 0.989375, 0.990525, 0.99165, 0.9928, 0.993475, 0.9939, 0.994725, 0.995125, 0.995725, 0.99595, 0.996525, 0.99695, 0.997175, 0.997375, 0.9976, 0.997975, 0.998125, 0.998375, 0.998625, 0.9988, 0.99895, 0.99905, 0.999075, 0.999225, 0.999325, 0.99935, 0.999425, 0.999475, 0.9995, 0.9995, 0.9996, 0.999625, 0.999625, 0.999625, 0.999675, 0.9997, 0.999725, 0.999725, 0.9998, 0.9998, 0.9998, 0.999875, 0.9999, 0.999925, 0.99995, 0.99995, 0.99995, 0.99995, 0.99995, 0.999975, 1.0], color="red", lw=4, label="4 neighbors")
    plt.plot([0.0, 0.00015, 0.0007, 0.001375, 0.003175, 0.00545, 0.008775, 0.014, 0.019975, 0.026325, 0.033325, 0.042675, 0.051975, 0.06315, 0.075375, 0.0883, 0.102125, 0.117625, 0.133075, 0.150225, 0.1675, 0.18655, 0.204525, 0.223775, 0.242425, 0.26175, 0.28005, 0.2988, 0.31745, 0.336325, 0.353925, 0.372825, 0.3908, 0.409275, 0.427925, 0.445225, 0.46355, 0.480525, 0.4984, 0.515675, 0.5344, 0.552675, 0.569775, 0.586125, 0.6025, 0.6212, 0.6376, 0.65325, 0.669225, 0.684675, 0.69995, 0.715775, 0.729875, 0.744725, 0.758625, 0.77325, 0.787475, 0.801125, 0.81435, 0.826825, 0.8388, 0.851425, 0.86215, 0.87175, 0.8808, 0.890025, 0.898975, 0.906825, 0.914775, 0.921875, 0.929, 0.935675, 0.941625, 0.946325, 0.9517, 0.9568, 0.960875, 0.964675, 0.96855, 0.971325, 0.974125, 0.9767, 0.978925, 0.981225, 0.9831, 0.98445, 0.986075, 0.98725, 0.988625, 0.9898, 0.990575, 0.991325, 0.99195, 0.9927, 0.9933, 0.993875, 0.99435, 0.9948, 0.99545, 0.99595, 0.9962, 0.996575, 0.997075, 0.9975, 0.99775, 0.998025, 0.9983, 0.998425, 0.99855, 0.998725, 0.99885, 0.999025, 0.999125, 0.99925, 0.999275, 0.999275, 0.99935, 0.99945, 0.999525, 0.99955, 0.99955, 0.9996, 0.99965, 0.999675, 0.999675, 0.9997, 0.99975, 0.999775, 0.999775, 0.999775, 0.999825, 0.99985, 0.999875, 0.9999, 0.9999, 0.999975, 1.0], color="orange", lw=4, label="8 neighbors")
    plt.legend()
    plt.xlabel("Time")
    plt.ylabel("Fraction of Recovered")
    plt.show()


grid = np.zeros((height, width))

#simulate_multiple_SIR()
# simulate_infectivities()
plot_neighbors()
