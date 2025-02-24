import numpy as np
import matplotlib.pyplot as plt
import random

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


def initialize_forest(seed=None):
    """Creates a forest grid with all trees and ignites one random tree."""
    if seed:
        np.random.seed(seed)
        random.seed(seed)

    forest = np.ones((GRID_SIZE, GRID_SIZE), dtype=int)  # All trees
    burn_time = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)  # Tracks how long a tree burns

    # Ignite a random tree
    x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
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


def simulate_wildfire(seed=None, continuous_plot=True):
    """Simulates wildfire spread over time."""
    forest, burn_time = initialize_forest(seed)

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
                        if seed:
                            # (Re)-Setting the seed inside the loop helps with reproducability for Dask
                            # This is being set here to be able to verify correctness. In actual simulation
                            # we can prevent any seed from being set to get true randomness.
                            random.seed(seed)
                        if forest[nx, ny] == TREE and random.random() < FIRE_SPREAD_PROB:
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


def run_n_simulations_default(n_simulations=1, seeds=None, no_print=False):
    """
    Runs n_simulations SERIALLY, and returns an average of the fire_spread over time that is obtained
    from each run. 
    seeds refers to an array of seeds, which MUST match the number of simulations. If provided, it is used
    to help with reproducability of the results
    """
    if seeds and len(seeds) != n_simulations:
        print("Number of seeds must match number of simulations")
        return

    all_results = []
    for i in range(n_simulations):
        curr_seed = None if not seeds else seeds[i]
        # Continuous plotting does not make a lot of sense when multiple simulations are being run.
        # So, we prevent doing that here.
        curr_spread = simulate_wildfire(curr_seed, continuous_plot=False)
        all_results.append(curr_spread)
        if not no_print:
            print(f"[SERIAL] Simulation {i} completed.")
    
    # Return the average of the individual simulations, where the average is taken over the columns
    # This is because each column represents a single day. 
    return np.array(all_results).mean(axis=0)

if __name__ == "__main__":
    # Run Multiple Simulations Serially
    fire_spread_over_time = run_n_simulations_default(n_simulations=5)

    # Plot results
    plt.figure(figsize=(8, 5))
    plt.plot(range(len(fire_spread_over_time)), fire_spread_over_time, label="Burning Trees")
    plt.xlabel("Days")
    plt.ylabel("Number of Burning Trees")
    plt.title("Wildfire Spread Over Time")
    plt.legend()
    plt.show()