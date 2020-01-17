# Created by Pro-Machina
# This algorithm finds the minimum for the function (x1 - 2)^2 + (x2 - 3)^2
# Answer should be x1 = 2 and x2 = 3
# This code is the simplest form of Genetic Algorithm

import math
import random

epsi = 2 # Precision level 

l = 30 # String length of x1 and/or x2
pm = 0.2 # Probability of mutaion to occur on a gene
iteration = 500 # Total iterations that the algorithm should run for

# x1 and x2 range from -4 to 4
# This range can be changed for each x1 and x2 separately depending on the problem
x1_min = -4
x2_min = -4
x1_max = 4
x2_max = 4

def calc_f (string, l, pre_post):
    """ To return the function value, input pre_post = 0 to iterate first half of the chromosome, 1 otherwise """

    if (pre_post == 0):
        var = string[:l]
        x_min = x1_min
        x_max = x1_max
    elif (pre_post == 1):
        var = string[l:]
        x_min = x2_min
        x_max = x2_max

    # d is the decoded value of the chromosome
    d = 0
    # x is the value of variable which depends on it's min and max value along with the length of the chromosome and the decoded value
    x = 0
    count = l - 1

    for bits in var:
        # This loop calculates the decimal value of the binary chromosome in iterative manner
        d = d + ( bits*(2**count) )
        count = count - 1
    #print(d)
    x = x_min + ( ( (x_max - x_min)/((2**l) - 1) )*d )
    
    if (pre_post == 0):
        #print ((x - 2)**2)
        return ( (x - 2)**2 )
    elif (pre_post == 1):
        #print ((x - 3)**2)
        return ( (x - 3)**2 ) 

def calc_x (string, l, pre_post):
    """ Calculate x value or decoded value of the chromosome """
    
    # The function is similar to calc_f function
    if (pre_post == 0):
        var = string[:l]
        x_min = x1_min
        x_max = x1_max
    elif (pre_post == 1):
        var = string[l:]
        x_min = x2_min
        x_max = x2_max

    d = 0
    x = 0
    count = l - 1

    for bits in var:
        d = d + ( bits*(2**count) )
        count = count - 1

    x = x_min + ( ( (x_max - x_min)/((2**l) - 1) )*d )
    return x

def rand_string (l):
    """ Assigns 0 or 1 with equal probability to a gene of a chromosome of length l """

    string = [0]*l
    for i in range(0, l):
        if random.uniform(0,1) < 0.5:
            string[i] = 0
        else:
            string[i] = 1

    return string

def single_point_crossover (mating_pool, mating_pool_size, l):
    """ Crossover from the mid-point of the string of the mating pool """

    i = 0
    temp_spc1 = [0] # Stores later half of the 1st chromosome
    temp_spc2 = [0] # Stores later half of the next chromosome
    return_pool = mating_pool
    while ( i < (mating_pool_size - 1) ):
        temp_spc1 = mating_pool[i][:l]  
        temp_spc2 = mating_pool[i+1][:l]

        return_pool[i][l:] = mating_pool[i][l:]
        return_pool[i][:l] = temp_spc2
        return_pool[i+1][l:] = mating_pool[i+1][l:]
        return_pool[i+1][:l] = temp_spc1

        i = i + 1
        #print (return_pool)
    return return_pool

def mutation (pool, pool_size, l, pm):
    """ Mutation occurs with a probability of pm on each gene of each chromosome in the pool """

    for chromes in pool:
        for gene in chromes:
            if random.uniform(0, 1) < pm:
                if ( gene == 1 ):
                    gene = 0
                else:
                    gene = 1
    return pool

def find_best_ans (pool, pool_size):
    """ From all the solutions, finds the index of the best solution in the pool """

    count = 0
    index = 0
    f_array_min = 10000000 # A large number so that every other number is smaller by default
    f_array = [0]*pool_size # f_array stores all the function values of the chromosomes
    for chromes in pool:
        # This loop finds the index of the chromosome with the best function value in the pool
        f_array[count] = calc_f(chromes, l, 0) + calc_f(chromes, l, 1)
        if ( f_array[count] < f_array_min ): 
            f_array_min = f_array[count]
            index = count

        count = count + 1

    return index

def check_entry (mating_pool, mating_pool_size):
    """ Function returns a true value if any chromosome in the pool is 0 """

    value = 0
    for i in range(0, mating_pool_size):
        if (mating_pool[i] == 0):
            value = 1
    return value

def stop_rep (pool, pool_size, l):
    """ If any repetation is present in the pool, the function repairs it """

    # This function just adds a redundancy to avoid a redundant solution        
    i = 0
    j = 0
    while (i < pool_size):
        while (j < pool_size):
            if (i != j):
                if (pool[i] == pool[j]):
                    pool[i] = rand_string(2*l)
            j = j + 1
        i = i + 1
    return pool
# End of function definitions
""""""
# Main program starts
pool_size = int(input('Enter the pool size: ')) # To get better accuracy, keep the pool size more than 100
mating_pool_size = pool_size # Mating pool is kept as big as the original pool, can be changed here
mating_pool = [0]*mating_pool_size  
pool = [0]*pool_size
f_array = [0]*pool_size
rank_count = 0
iter_algo = 0

for i in range(0, pool_size):
    # The loop adds an initial random population in the pool
    pool[i] = rand_string(2*l)
    rank_count = rank_count + 1

while(iter_algo < iteration):
    pool = stop_rep(pool, pool_size, l)
    count = 0
    for chrom in pool:
        f_array[count] = calc_f(chrom, l, 0) + calc_f(chrom, l, 1)
        count = count + 1

    # Sort the pool along with it's f values from best to worst
    temp1 = 0
    temp2 = [0]*2*l
    swap = 1
    while(swap >= 0):
        for i in range( 0, (pool_size-1) ):
            if (f_array[i + 1] < f_array[i]):
                temp1 = f_array[i + 1]
                f_array[i + 1] = f_array[i]
                f_array[i] = temp1

                temp2 = pool[i + 1]
                pool[i + 1] = pool[i]
                pool[i] = temp2

                swap = swap + 1
            else:
                swap = swap - 1

    # We go by ranking selection to select for mating
    val = True
    j = 0
    while (val):
        if (check_entry(mating_pool, mating_pool_size) == 1):
            for i in range(0, pool_size):
                if (random.uniform(0, 1) < i/rank_count):
                    if (j < mating_pool_size):
                        mating_pool[j] = pool[i] # Mating pool is filled with best solution at the top (redundancy to sorting)
                    j = j + 1
        else:
            val = False            

    pool = single_point_crossover(mating_pool, mating_pool_size, l) # Returned pool has two best solutions crossover at the top and follows similar pattern to the worst solution at the bottom
    pool = mutation (pool, pool_size, l, pm)

    iter_algo = iter_algo + 1

index = find_best_ans (pool, pool_size) # To find the best solution in the pool generated
print ("From the Genetic Algorithm, the best solution is:") 
x1 = calc_x (pool[index], l, 0)
x2 = calc_x (pool[index], l, 1)
print ("x1: %f, x2: %f" % (x1, x2))
print ('Given function was: (x1-2)^2 + (x2-3)^2')
