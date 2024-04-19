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
    if seed is not None:
        random.seed(seed)
    infected_nodes = [(random.randint(0, lattice.height - 1), random.randint(0, lattice.width - 1)) for _ in range(num_infected)]
    lattice.infect_nodes(infected_nodes)


def run_step(lattice, infection_probability, recover_probability, recover_rate):
    is_process_alive = False
    infected_nodes = lattice.get_infected_nodes()
    new_infected = []
    for infected_node in infected_nodes:
        # INFECT NEIGHBORS
        neighbors = lattice.get_susceptible_neighbors(infected_node)
        for neighbor in neighbors:
            if infection_probability > lattice.randoms[neighbor]:
                new_infected.append(neighbor)
        # RECOVER
        if recover_probability > lattice.randoms[infected_node] and lattice.infection_time[infected_node] > 1./recover_rate:
            lattice.recover_node(infected_node)

        lattice.infection_time[infected_node] += 1

    if len(new_infected) > 0:
        is_process_alive = True
        lattice.infect_nodes(new_infected)
    data = lattice.get_data()
    return data, is_process_alive


def run_simulation(lattice, num_infected, infection_probability, recover_probability, recover_rate, seed=None):
    infect_random(lattice, num_infected, seed)
    active = True
    susceptible_data = []
    infected_data = []
    recovered_data = []
    with plt.ion():
        fig = plt.figure()
        im = plt.imshow(lattice.grid, cmap="viridis", vmin=0, vmax=2)
        while active:
            realtime_data, active = run_step(lattice, infection_probability, recover_probability, recover_rate)
            susceptible_data.append(realtime_data[0])
            infected_data.append(realtime_data[1])
            recovered_data.append(realtime_data[2])
            im.set_data(lattice.grid)
            fig.canvas.flush_events()
            plt.pause(0.1)
    print(lattice.grid)
    plot_simulation(susceptible_data, infected_data, recovered_data)
    return infected_data


def plot_simulation(susceptible_data, infected_data, recovered_data):
    plt.figure()
    plt.plot(infected_data, alpha=0.5, lw=2, label="Infected", color="red")
    plt.plot(susceptible_data, alpha=0.5, lw=2, label="Susceptible", color="blue")
    plt.plot(recovered_data, alpha=0.5, lw=2, label="Recovered", color="green")
    plt.xlabel("Time")
    plt.title("SIR")
    plt.legend()
    plt.show()


def run_multiple_simulations(lattice, num_infected, num_simulations=10, seed=None):
    simulations_data = []
    infection_probabilities = np.linspace(0.1, 1.0, num_simulations)
    for prob in infection_probabilities:
        infected_data = run_simulation(lattice, num_infected, prob, seed)
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
    run_simulation(lattice, opt["num_infected"], opt["infection_probability"], opt["recover_probability"], opt["recover_rate"], opt["seed"])
    #run_multiple_simulations(lattice, opt["num_infected"], opt["num_simulations"], opt["seed"])


