from evaluator import evaluate
from evolve import evolve, splitlist
from sampler import sample
from settings import n, k, evo_duration
from program_manager import saveprogram
import threading, time, os, random

# chunkify

def chunks(l, n):
    newn = int(len(l) / n)
    for i in range(0, n - 1):
        yield l[i * newn: i * newn + newn]
    yield l[n * newn - newn:]

# get initial programs

init_programs = []
for file in os.listdir("./init_programs"):
    init_programs.append(int(file))
init_programs_per_island = []
while len(init_programs_per_island) < n:
    temp_init_programs = init_programs
    island_init_programs = []
    while island_init_programs < k:
        chosen_program = random.choice(temp_init_programs)
        temp_init_programs.remove(chosen_program)
        island_init_programs.append(chosen_program)
    init_programs_per_island.append(island_init_programs)

# store programs into respective islands

island_no_for_init = 1
for island in init_programs_per_island:
    island_program_id_for_init = 1
    for program_id in island:
        with open(f"./init_programs/{program_id}.py", "r") as f:
            program = f.read()
            saveprogram(island_program_id_for_init, program, island_no_for_init)
        island_program_id_for_init = island_program_id_for_init + 1
    island_no_for_init = island_no_for_init + 1

# initialise islands
# all_islands: {1 # island no.: {signature: [id1, id2, id3, ...], ...}, ...}

all_islands = {}
for island_id in range(1, n + 1):
    score1 = evaluate(ids = 1, island_id = island_id)
    score2 = evaluate(ids = 2, island_id = island_id)
    

# get next ID

def get_next_ID(all_islands):
    IDlist = []
    for island in list(all_islands.values()):
        for signature in list(island.values()):
            for ids in signature:
                IDlist.append(ids)
    return max(IDlist) + 1

# evolution

def evolve_island(island):
    starttime = time.perf_counter()
    time_passed = 0
    while time_passed < evo_duration:
        new_programs = evolve(island)
        for program in new_programs:
            program_id = get_next_ID(all_islands)
            saveprogram(program_id, program)
            program_score = evaluate(program = program)
            