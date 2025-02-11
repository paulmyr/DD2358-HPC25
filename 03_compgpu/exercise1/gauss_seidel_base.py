import numpy as np

# Constants
NUM_ITERATIONS = 100

# @profile
def gauss_seidel(f):
    """
    The simple, base, version of the gauss_seidel solver provided
    to us in the assignment description.
    """
    newf = f.copy()
    
    for i in range(1,newf.shape[0]-1):
        for j in range(1,newf.shape[1]-1):
            newf[i,j] = 0.25 * (newf[i,j+1] + newf[i,j-1] +
                                   newf[i+1,j] + newf[i-1,j])
    
    return newf

# @profile
def solve_posisson(base_grid, num_iters):
    """
    Calls the gauss_seidel method on the grid "num_iters" number of times.
    The grid should be initialized properly (ie, must be a square grid with 0s
    at the boundary.)

    The grid utilized here is initialzied using numpy
    """
    for i in range(num_iters):
        base_grid = gauss_seidel(base_grid)
    
    return base_grid

    

# COMMENTING OUT TO NOT INTERFERE WITH TESTS
# if __name__ == "__main__":
#     grid_size = 10
#     # Generate the grid (square, with 0s at the boundary)
#     base_grid = np.zeros((grid_size, grid_size))
#     base_grid[1:-1, 1:-1] = np.random.rand(grid_size-2, grid_size-2)

#     # Run
#     print(f"Running Gauss-Seidel Solver with grid: {grid_size} and iters: {NUM_ITERATIONS}")
#     result = solve_posisson(base_grid=base_grid, num_iters=NUM_ITERATIONS)
