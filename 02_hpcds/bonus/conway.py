"""
conway.py 

A simple Python/matplotlib implementation of Conway's Game of Life.

Author: Mahesh Venkitachalam
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

ON = 255
OFF = 0
vals = [ON, OFF]


def random_grid(n):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, n * n, p=[0.2, 0.8]).reshape(n, n)


def add_glider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0, 0, 255], [255, 0, 255], [0, 255, 255]])
    grid[i : i + 3, j : j + 3] = glider


def add_gosper_glider_gun(i, j, grid):
    """adds a Gosper Glider Gun with top left cell at (i, j)"""
    gun = np.zeros(11 * 38).reshape(11, 38)

    gun[5][1] = gun[5][2] = 255
    gun[6][1] = gun[6][2] = 255

    gun[3][13] = gun[3][14] = 255
    gun[4][12] = gun[4][16] = 255
    gun[5][11] = gun[5][17] = 255
    gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = 255
    gun[7][11] = gun[7][17] = 255
    gun[8][12] = gun[8][16] = 255
    gun[9][13] = gun[9][14] = 255

    gun[1][25] = 255
    gun[2][23] = gun[2][25] = 255
    gun[3][21] = gun[3][22] = 255
    gun[4][21] = gun[4][22] = 255
    gun[5][21] = gun[5][22] = 255
    gun[6][23] = gun[6][25] = 255
    gun[7][25] = 255

    gun[3][35] = gun[3][36] = 255
    gun[4][35] = gun[4][36] = 255

    grid[i : i + 11, j : j + 38] = gun


def update(frame_num, img, grid, n):
    """
    Updates the grid by applying the rules of Conway's Game of Life. The rules for the game
    and more information on it can be found here:
    https://www.geeksforgeeks.org/conways-game-life-python-implementation/
    """
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line
    new_grid = grid.copy()
    for i in range(n):
        for j in range(n):
            # compute 8-neghbor sum
            # using toroidal boundary conditions - x and y wrap around
            # so that the simulaton takes place on a toroidal surface.
            total = int(
                (
                    grid[i, (j - 1) % n]
                    + grid[i, (j + 1) % n]
                    + grid[(i - 1) % n, j]
                    + grid[(i + 1) % n, j]
                    + grid[(i - 1) % n, (j - 1) % n]
                    + grid[(i - 1) % n, (j + 1) % n]
                    + grid[(i + 1) % n, (j - 1) % n]
                    + grid[(i + 1) % n, (j + 1) % n]
                )
                / 255
            )
            # apply Conway's rules
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    new_grid[i, j] = OFF
            else:
                if total == 3:
                    new_grid[i, j] = ON
    # update data
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return (img,)


# main() function
def main():
    """
    This function is responsible for accepting arguments from the command line (such as grid size
    and other initialization information for the grid) and for running the game of life, including
    the animation involved.
    """
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(
        description="Runs Conway's Game of Life simulation."
    )
    # add arguments
    parser.add_argument("--grid-size", dest="n", required=False)
    parser.add_argument("--mov-file", dest="movfile", required=False)
    parser.add_argument("--interval", dest="interval", required=False)
    parser.add_argument("--glider", action="store_true", required=False)
    parser.add_argument("--gosper", action="store_true", required=False)
    args = parser.parse_args()

    # set grid size
    n = 512
    if args.n and int(args.n) > 8:
        n = int(args.n)

    # set animation update interval
    update_interval = 50
    if args.interval:
        update_interval = int(args.interval)

    # declare grid
    grid = np.array([])
    # check if "glider" demo flag is specified
    if args.glider:
        grid = np.zeros(n * n).reshape(n, n)
        add_glider(1, 1, grid)
    elif args.gosper:
        grid = np.zeros(n * n).reshape(n, n)
        add_gosper_glider_gun(10, 10, grid)
    else:
        # populate grid with random on/off - more off than on
        grid = random_grid(n)

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation="nearest")
    ani = animation.FuncAnimation(
        fig,
        update,
        fargs=(
            img,
            grid,
            n,
        ),
        frames=10,
        interval=update_interval,
        save_count=50,
    )

    # # of frames?
    # set output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=["-vcodec", "libx264"])

    plt.show()


# call main
if __name__ == "__main__":
    main()
