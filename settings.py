# ALL THESE VALUES ARE TAKEN FROM THE FUNSEARCH PAPER

# sampling
T_0 = 0.1 # initial cluster probability temperature
N = 30000 # cluster probability temperature period
T_program = 1.0 # program probability temperature

# evolution
k = 2 # how many programs to include in a prompt
n = 10 # how many islands to run
evo_duration = 60 * 60 * 4 # how long to evolve an island in seconds
max_threads_per_island = 16 # how many threads to run for every single island