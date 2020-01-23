# Created by Pro-Machina
# This is an implementation of Particle Swarm Optimisation algorithm for the function:
# Maximize: f(x) = 1 - (x^2) + 2x
# Matrices are classified into position and fitness matrices, majorly only position matrices are used

import numpy as np
import random

# Paramenters are taken as
w = 0.7 # Inertia weight (larger -> greater global search, smaller -> greater local search)
c1 = 0.2 # Acceleratin coefficient 1
c2 = 0.6 # Acceleration coefficient 2
iterations = 100 # Number of iterations to go through
# (c1 > c2 : greater local search ability)
# (c2 > c1 : greater global search ability)

def find_fitness (swarm_pos):
    """ Finds the fitness of the swarm with respect to their positions """
    # This function needs to be updated after changing the fitness function

    swarm_size = int(np.shape(swarm_pos)[0])
    if (np.ndim(swarm_pos) > 1):
        # Since global best is also an input in this function and it's a 1D array, the below line of code would give an error if the condition is not implemented
        n_var = int(np.shape(swarm_pos)[1])

    swarm_fit = np.zeros((swarm_size, 1))
    for r in range(0, swarm_size):
        swarm_fit[r] = 1 - ((swarm_pos[r])**2) + (2*(swarm_pos[r])) # Make changes here if there is any change in fitness function
        if (np.ndim(swarm_pos) > 1):
            # Seperately adding the column index for array with more than 1 dimensions
            swarm_fit[r] = 1 - ((swarm_pos[r][0])**2) + (2*(swarm_pos[r][0])) # Make changes here if there is any change in fitness function

    # Swarm fitness is a (swarm_size X 1) dimensional fitness matrix
    return swarm_fit

def find_global_best (swarm_pos, global_best, max_min = 'max'):
    """ Finds the global best and returns the corresponding position, enter 'min' if its a minimisation problem, 'max' otherwise """

    swarm_fit = find_fitness(swarm_pos)
    swarm_size = int(np.shape(swarm_pos)[0])
    n_var = int(np.shape(swarm_pos)[1])


    if (max_min == 'min'):
        for r in range(0, swarm_size):
            if (float(swarm_fit[r][0]) < float(find_fitness(global_best)[0])):
                global_best = (swarm_pos[r][:]).copy()
    else:
        for r in range(0, swarm_size):
            if (float(swarm_fit[r][0]) > float(find_fitness(global_best)[0])):
                global_best = (swarm_pos[r][:]).copy()

    # Global best is a (1 X n_var) dimensional position matrix
    return global_best

def find_local_best (swarm_pos, local_best, max_min = 'max'):
    """ Keeps a track of the personal best of a swarm and returns the same, enter 'min' if its a minimisation problem, 'max' otherwise """

    swarm_fit = find_fitness(swarm_pos)
    swarm_size = int(np.shape(swarm_pos)[0])
    n_var = int(np.shape(swarm_pos)[1])

    if (max_min == 'min'):
        for r in range(0, swarm_size):
            for c in range(0, n_var):
                if (float(swarm_fit[r][0]) < float(find_fitness(local_best[r][:])[0])):
                    local_best[r][:] = (swarm_pos[r][:]).copy()
    else:
        for r in range(0, swarm_size):
            for c in range(0, n_var):
                if (float(swarm_fit[r][0]) > float(find_fitness(local_best[r][:])[0])):
                    local_best[r][:] = (swarm_pos[r][:]).copy()

    # Local besst is a (swarm_size X n_var) dimensional position matrix
    return local_best

def update_vel (swarm_vel, swarm_pos, global_best, local_best ):
    """ Returns the updated velocity vector for each swarm particle """

    r1 = random.uniform(0, 1)
    r2 = random.uniform(0, 1)
    new_vel = swarm_vel.copy()
    swarm_size = int(np.shape(swarm_pos)[0])
    n_var = int(np.shape(swarm_pos)[1])

    for r in range(0, swarm_size):
        for c in range(0, n_var):
            new_vel[r][c] = (w*swarm_vel[r][c]) + ( c1*( r1*(local_best[r][c] - swarm_pos[r][c]) ) ) + ( c2*( r2*(global_best[0] - swarm_pos[r][c]) ) )
            if (n_var > 1):
                new_vel[r][c] = (w*swarm_vel[r][c]) + ( c1*( r1*(local_best[r][c] - swarm_pos[r][c]) ) ) + ( c2*( r2*(global_best[0][c] - swarm_pos[r][c]) ) )

    # New velocity is a (swarm_size X n_var) dimensional position type matrix
    return new_vel

def update_position (swarm_pos, swarm_vel):
    """ Returns the updated position of the swarm particles """

    swarm_size = int(np.shape(swarm_pos)[0])
    n_var = int(np.shape(swarm_pos)[1])
    new_pos = swarm_pos.copy()

    for r in range(0, swarm_size):
        for c in range(0, n_var):
            new_pos[r][c] = swarm_pos[r][c] + swarm_vel[r][c]

    # New position is a (swarm_size X n_var) dimensional position matrix
    return new_pos


# Main program starts
swarm_size = int(input('Enter the swarm size: '))
n_var = int(input('Enter the number of variables: '))

var_range = np.zeros((n_var, 2))
for r in range(0, n_var):
    var_range[r][0] = float(input('Enter min value for variable %d: ' % (r+1)))
    var_range[r][1] = float(input('Enter max value for variable %d: ' % (r+1)))

# Initialize the swarm particles' positions
swarm_pos = np.zeros((swarm_size, n_var))
#print(swarm_pos)
for r in range(0, swarm_size):
    for c in range(0, n_var):
        swarm_pos[r][c] = random.uniform(var_range[c][0], var_range[c][1])

# Initialize the swarm particles' velocity
swarm_vel = np.zeros((swarm_size, n_var))
for r in range(0, swarm_size):
    for c in range(0, n_var):
        swarm_vel[r][c] = random.uniform(-1, 1)

# Start the iterations
global_best = np.zeros((1, n_var))
local_best = np.zeros((swarm_size, n_var))

while (iterations > 0):

    global_best = find_global_best(swarm_pos, global_best, max_min = 'max')
    local_best = find_local_best(swarm_pos, local_best, max_min = 'max')
    swarm_vel = update_vel(swarm_vel, swarm_pos, global_best, local_best)
    swarm_pos = update_position(swarm_pos, swarm_vel)

    iterations = iterations - 1 

print('')
print('Converging through Particle Swarm Optimization')   
print('')
print('The Final Solution is: %f' % global_best)
print('')
print('The value of thee function at this position is: %f' % find_fitness(global_best))
print('')
