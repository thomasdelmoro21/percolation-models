"""
@author Thomas Del Moro
"""

import yaml
import random
import matplotlib.pyplot as plt

from grid import Lattice


def infect_random(lattice, num_infected):
    random.seed(110)
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
    return is_process_alive


def run_simulation(lattice, num_infected, infection_probability):
    infect_random(lattice, num_infected)
    active = True
    plt.ion()
    fig = plt.figure()
    im = plt.imshow(lattice.grid, cmap="viridis")
    while active:
        active = invade(lattice, infection_probability)
        im.set_data(lattice.grid)
        fig.canvas.flush_events()
        plt.pause(0.1)


if __name__ == '__main__':
    with open('config.yml', 'rb') as f:
        opt = yaml.safe_load(f.read())

    lattice = Lattice(opt["width"], opt["height"])
    run_simulation(lattice, opt["num_infected"], opt["probability"])
