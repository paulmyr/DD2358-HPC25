from multiprocessing import Pool

import numpy as np
import matplotlib.pyplot as plt
import random

import pdb

# Constants
GRID_SIZE = 800  # 800x800 forest grid
FIRE_SPREAD_PROB = 0.3  # Probability that fire spreads to a neighboring tree
BURN_TIME = 3  # Time before a tree turns into ash
DAYS = 60  # Maximum simulation time

# State definitions
EMPTY = 0  # No tree
TREE = 1  # Healthy tree
BURNING = 2  # Burning tree
ASH = 3  # Burned tree


def initialize_forest(custom_rand):
    """Creates a forest grid with all trees and ignites one random tree."""

    forest = np.ones((GRID_SIZE, GRID_SIZE), dtype=int)  # All trees
    burn_time = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)  # Tracks how long a tree burns

    # Ignite a random tree
    x, y = custom_rand.randint(0, GRID_SIZE - 1), custom_rand.randint(0, GRID_SIZE - 1)
    forest[x, y] = BURNING
    burn_time[x, y] = 1  # Fire starts burning

    return forest, burn_time


def get_neighbors(x, y):
    """Returns the neighboring coordinates of a cell in the grid."""
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            neighbors.append((nx, ny))
    return neighbors

def simulate_wildfire(seed=None, continuous_plot=False):
    """Simulates wildfire spread over time."""
    custom_rand = random.Random(seed)
    forest, burn_time = initialize_forest(custom_rand)

    fire_spread = []  # Track number of burning trees each day

    for day in range(DAYS):
        new_forest = forest.copy()

        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if forest[x, y] == BURNING:
                    burn_time[x, y] += 1  # Increase burn time

                    # If burn time exceeds threshold, turn to ash
                    if burn_time[x, y] >= BURN_TIME:
                        new_forest[x, y] = ASH

                    # Spread fire to neighbors
                    for nx, ny in get_neighbors(x, y):
                        if forest[nx, ny] == TREE and custom_rand.random() < FIRE_SPREAD_PROB:
                            new_forest[nx, ny] = BURNING
                            burn_time[nx, ny] = 1

        forest = new_forest.copy()
        fire_spread.append(np.sum(forest == BURNING))

        if np.sum(forest == BURNING) == 0:  # Stop if no more fire
            if day < DAYS - 1:
                fire_spread += [0 for _ in range(DAYS - 1 - day)]
            break

        # Plot grid every 5 days
        if continuous_plot and (day % 5 == 0 or day == DAYS - 1):
            plt.figure(figsize=(6, 6))
            plt.imshow(forest, cmap='viridis', origin='upper')
            plt.title(f"Wildfire Spread - Day {day}")
            plt.colorbar(label="State: 0=Empty, 1=Tree, 2=Burning, 3=Ash")
            plt.show()

    return fire_spread

def run_n_simulations_parallel(n_simulations=1, seeds=None, show_line_plot=False, no_print=False):
    """
    Runs n_simulations PARALLELY, using the multiprocessing module, and returns an average of the fire_spread over time that is 
    obtained from each run.
    seeds refers to an array of seeds, which MUST match the number of simulations. If provided, it is used
    to help with reproducability of the results
    """
    if seeds and len(seeds) != n_simulations:
        print("Number of seeds must match number of simulations")
        return
    
    with Pool(n_simulations) as pool:
        fire_spread_over_time = pool.map(simulate_wildfire, seeds)

    if show_line_plot:
        for i in range(n_simulations):
            plt.plot(range(len(fire_spread_over_time[i])), fire_spread_over_time[i], label=f"Simulation no: {i}",  alpha=0.3, linestyle="--")
    
    # Return the mean of the spread for each day obtained over the number of simulations
    return np.array(fire_spread_over_time).mean(axis=0)


# Run simulation
if __name__ == "__main__":
    # Run Multiple Simulations in Parallel using Multiprocessing
    fire_spread_over_time = run_n_simulations_parallel(n_simulations=5, seeds=[i for i in range(5)], show_line_plot=True)

    # Plot results
    plt.plot(range(len(fire_spread_over_time)), fire_spread_over_time, label="Average Burning Trees")
    plt.xlabel("Days")
    plt.ylabel("Number of Burning Trees")
    plt.title("Wildfire Spread Over Time [Multiprocessing]")
    plt.legend()
    plt.show()