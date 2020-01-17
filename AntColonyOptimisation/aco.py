# Created by Pro-Machina
# Ant Colony Optimization in Traveling Salesman Problem
# Assuming that the salesman has to start from a given city (input) and has to return to the same city at the end of the trip ..
# and all the costs are symmetric, i.e, cost for traveling from city i to j is same as that of traveling from city j to i ..
# each city can be visited only once

import numpy as np # Major use: Arrays and Matrices
import random # Major use: Random number generation

tau = 100 # Initial pheromone value of arc between cities
ants = 9000 # Number of ants (iterations), this becomes the termination criteria
rho = 0 # Evaporation coefficient (if taken 0, its for simplicity)
alpha = 1 # Alpha value, used in probability calculation
beta = 1 # Beta value, used in probability calculation
q = 1000 # Pheromone count (used while updating the phromone of the arcs after an iteration)
k = 0.2 # Distance to cost conversion parameter C = k*D (Assumed linear behaviour)

def prob (no_city, dist_array, tau_array, city_trav):
    """ Returns a matrix that has values of probability of an ant travelling between two cities """

    # We alter the distance and pheromone array such that values corresponding to cities already traveled are 0
    # The formula for probability of traveling between city i and j is given by:
    #               (Tij(t)^a)/(dij(t)^b)
    # Pij(t) = ----------------------------------  Where T: tau, d: distance or cost, a: alpha, b: beta, t: t-th iteration of the algorithm 
    #           sum-j( (Tij(t)^a)/(dij(t)^b) )           
    
    temp_dist = dist_array.copy() # Note: .copy() is necessary to avoid changes in the original matrix
    temp_tau = tau_array.copy()
    last_city = 0
    index = 0
    for i in range(0, no_city):
        if (city_trav[i] != 0):
            index = city_trav[i] - 1
            temp_dist[:, index] = 0
            temp_tau[:, index] = 0
    
    sum_prob = 0
    prob_array = np.zeros(no_city) # The array contains probability of travelling between two cities
    for c in range(0, no_city):
        if (temp_dist[index][c] != 0):
            prob_array[c] = ((temp_tau[index][c])**alpha)/((temp_dist[index][c])**beta)
            sum_prob = sum_prob + prob_array[c]
    if (sum_prob != 0):
        prob_array = prob_array/sum_prob

    return prob_array

def city_selection (prob_array):
    """ Returns the next city number based on roulette wheel selection """

    col = int(np.shape(prob_array)[0]) # Number of columns in prob_array
    rand = random.uniform(0, 1) # Random number generation
    roulette = 0
    for c in range(0, col):
        if (prob_array[c] != 0):
            if ( (rand > roulette) & (rand < (roulette + prob_array[c])) ):
                return (c+1) # (c+1) is the required city number
        roulette = roulette + prob_array[c]        

def total_cost (city_trav, dist_array):
    """ Calculates the total cost of travel, based on total distance travelled """

    col = int(np.shape(city_trav)[0]) 
    total_dist = 0
    end_city = 0
    for c in range(0, (col-1)):
        total_dist = total_dist + dist_array[city_trav[c] - 1][city_trav[c+1] - 1] 
    end_city = city_trav[col-1] - 1
    total_dist = total_dist + dist_array[city_trav[0]][end_city] # Accounts for returning to the base city

    return (k*total_dist)

def pheromone_update (city_trav, dist_array, tau_array):
    """ Updates the pheromone for the arcs between the cities """

    new_tau = q/total_cost(city_trav, dist_array) # Updates the value based on total cost of the route
    col = int(np.shape(city_trav)[0])
    r = 0
    k = 0
    for c in range(0, (col-1)):
        r = (city_trav[c] - 1)
        k = (city_trav[c+1] - 1)
        tau_array[r][k] = ((1-rho)*tau_array[r][k]) + new_tau
        tau_array[k][r] = tau_array[r][k] # To preserve symmetry in the matrix

    return tau_array


# Main program starts
no_city = int(input('Enter the number of cities: ')) # Input the number of cities in the problem
start_city = int(input('Enter the starting city: ')) # Salesman starts from tis city
dist_array = np.zeros((no_city, no_city)) # The array is the matrix of distance between the cities
tau_array = np.zeros((no_city, no_city)) # The array contains feromone values of arcs between the cities
city_trav = np.zeros(no_city)
city_trav = city_trav.astype(int) # Necessary to make the values integer, so that the city numbers could be used as an index for other matrices

# The following loop takes input to fill up the distance matrix and sets initial values for other matrices
# Initialising segment
for r in range(0, no_city):
    for c in range(0, no_city):
        if (dist_array[r][c] == 0):
            if (r != c):
                tau_array[r][c] = tau # Initialise the pheromone values
                tau_array[c][r] = tau_array[r][c] # To preserve symmetry
                dist_array[r][c] = float(input('Enter distance for city ' + str(r+1) + ', city ' + str(c+1) + ' : '))
                dist_array[c][r] = dist_array[r][c] # Distance matrix is a symmetric matrix

while(ants > 0):
    city_trav = np.zeros(no_city)
    city_trav = city_trav.astype(int)
    city_trav[0] = start_city

    for c in range(0, no_city):
        if ( city_trav[c] == 0 ):
            city_trav[c] = city_selection(prob(no_city, dist_array, tau_array, city_trav))

    tau_array = pheromone_update(city_trav, dist_array, tau_array)
    ants = ants - 1

city_trav = np.append(city_trav, [start_city])
print ('The final path generated by Ant Colony Optimization is: ')
print (city_trav)
