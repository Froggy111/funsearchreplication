from evaluator import evaluate
from evolve import evolve, splitlist
from sampler import sample
from settings import n, k, evo_duration
from program_manager import saveprogram, readprogram
import threading, time, os, random, queue, json, glob

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
            f.close()
        island_program_id_for_init = island_program_id_for_init + 1
    island_no_for_init = island_no_for_init + 1

# initialise islands
# all_islands: {1 # island no.: {signature: [id1, id2, id3, ...], ...}, ...}

all_islands = {}
for island_id in range(1, n + 1):
    for program_id in range(1, k + 1):
        score = evaluate(ids = program_id, island_id = island_id)
        if score in list(all_islands[island_id].keys()):
            all_islands[island_id][score].append(program_id)
        else:
            all_islands[island_id][score] = [program_id]

# get next ID

def get_next_ID(island):
    IDlist = []
    for signature in list(island.values()):
        for ids in signature:
            IDlist.append(ids)
    return max(IDlist) + 1

# evolution

def evolve_island(island, queue):
    starttime = time.perf_counter()
    time_passed = 0
    while time_passed < evo_duration:
        new_programs = evolve(island)
        for program in new_programs:
            program_id = get_next_ID(island)
            saveprogram(program_id, program)
            program_score = evaluate(program = program)
            if program_score in list(island.keys()):
                island[program_score].append(program_id)
            else:
                island[program_score] = [program_id]
        time_passed = time.perf_counter() - starttime
    queue.put(island)

# keep evolving until stopped

iteration = 0
while True:
    iteration = iteration + 1
    all_islands_maxscores = {}
    queue = queue.Queue()
    pool = []

    # run evolve_island threads
    for island in list(all_islands.values()):
        thread = threading.Thread(target = evolve_island, args = [island, queue])
        pool.append(thread)
    island_id = 1
    for thread in pool:
        thread.start()
        response = queue.get()
        print(f"island {island_id} has evolved")
        all_islands[island_id] = response
        island_id = island_id + 1
    for thread in pool:
        thread.join()
    
    # get useful information from islands
    island_id = 1
    for island in all_islands:
        scores = [sum(x) / len(x) for x in list(island.keys())]
        maxscore = max(scores)
        maxscore_indices = [i for i, x in enumerate(scores) if x == maxscore]
        maxscore_program_ids = []
        for index in maxscore_indices:
            maxscore_program_ids.append(list(island.keys())[index])
        all_islands_maxscores[island_id] = {"maxscore": maxscore, "maxscore_program_ids": maxscore_program_ids}
    
    # dump useful information into file for human reference
    with open("./top_programs.txt", "a") as f:
        f.write(f"ITERATION: {iteration}\n\n" + json.dumps(all_islands_maxscores) + "\n\n")
        f.close()
    
    # get islands with lower score than half
    scorelist = [x["maxscore"] for x in list(all_islands_maxscores.values())]
    scorelist.sort()
    halfscore = scorelist[n / 2]
    island_id = 1
    bad_islands = []
    good_islands = []
    for island in list(all_islands_maxscores.values()):
        if island["maxscore"] < scorelist:
            bad_islands.append(island_id)
        else:
            good_islands.append(island_id)
    for island_id in bad_islands:
        files = glob.glob(f"./{island_id}/*")
        for f in files:
            os.remove(f)
        all_islands[island_id] = {}
    
    # sample islands
    seeds = []
    for island_id in good_islands:
        island = all_islands[island_id]
        seed = sample(island, island_id)
        seeds.append([island_id, seed])
    for island_id in bad_islands:
        chosen_seed = random.choice(seeds)
        seed_id = 1
        for parent in chosen_seed[1]:
            parent_program = readprogram(parent[0], chosen_seed[0])
            saveprogram(seed_id, parent_program, island_id)
            seed_id = seed_id + 1
            if score in list(all_islands[island_id].keys()):
                all_islands[island_id][parent[1]].append(seed_id)
            else:
                all_islands[island_id][parent[1]] = [seed_id]
    
    # safely stop if requested
    with open("./stop.txt", "r") as f:
        stop_signal = f.read()
        f.close()
    if stop_signal == "stop":
        break