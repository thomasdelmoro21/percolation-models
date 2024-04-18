"""
@author Thomas Del Moro
"""

import random
import matplotlib.pyplot as plt
import numpy as np
import yaml
import statistics

from grid import Lattice


def infect_random(lattice, num_infected, seed):
    if seed:
        random.seed(seed)
    infected_nodes = [(random.randint(0, lattice.height - 1), random.randint(0, lattice.width - 1)) for _ in range(num_infected)]
    lattice.infect_nodes(infected_nodes)


def invade(lattice, probability):
    is_process_alive = False
    new_infected = []
    for infected_node in lattice.get_infected_nodes():
        print(infected_node)
        neighbors = lattice.get_susceptible_neighbors(infected_node)
        for neighbor in neighbors:
            if probability > lattice.randoms[neighbor]:
                new_infected.append(neighbor)
    if len(new_infected) > 0:
        is_process_alive = True
        lattice.infect_nodes(new_infected)
    infected_fraction = lattice.get_infected_fraction()
    return infected_fraction, is_process_alive


def run_simulation(lattice, num_infected, infection_probability, seed=None):
    infect_random(lattice, num_infected, seed)
    active = True
    infected_data = []
    with plt.ion():
        fig = plt.figure()
        im = plt.imshow(lattice.grid, cmap="viridis")
        while active:
            infected_fraction, active = invade(lattice, infection_probability)
            infected_data.append(infected_fraction)
            im.set_data(lattice.grid)
            fig.canvas.flush_events()
            #plt.pause(0.1)
    plt.figure()
    plt.plot(infected_data, 'o', label="Infected sites", color="red")
    plt.ylabel("Infected fraction")
    plt.xlabel("Time")
    plt.title("SIR p={}".format(infection_probability))
    plt.show()


def run_multiple_simulations(lattice, num_infected, num_simulations=10, seed=None):
    simulations_data = []
    infection_probabilities = np.linspace(0.1, 1.0, num_simulations)
    for prob in infection_probabilities:
        infect_random(lattice, num_infected, seed + i if seed else None)
        active = True
        infected_data = []
        with plt.ion():
            fig = plt.figure()
            plt.title("SIR p={}".format(round(prob, 2)))
            im = plt.imshow(lattice.grid, cmap="viridis")
            while active:
                infected_fraction, active = invade(lattice, prob)
                infected_data.append(infected_fraction)
                im.set_data(lattice.grid)
                fig.canvas.flush_events()
        lattice.reset()
        simulations_data.append(infected_data[-1])
    print(simulations_data)
    plt.figure()
    plt.plot(infection_probabilities, simulations_data, 'o', label="Infected sites", color="red")
    plt.ylabel("Infected fraction")
    plt.xlabel("Infectivity")
    plt.title("SIR runs={}".format(num_simulations))
    plt.show()


if __name__ == '__main__':
    with open('config.yml', 'rb') as f:
        opt = yaml.safe_load(f.read())

    lattice = Lattice(opt["width"], opt["height"], opt["eight_neighbors"])
    run_multiple_simulations(lattice, opt["num_infected"], opt["num_simulations"], opt["seed"])


