from api import callLLM
from prompt import getprompt
from settings import k, max_threads_per_island
from parse_response import parse_response
import random, threading, queue

# split programs into groups
def splitlist(l, k): 
    for i in range(0, len(l), k):  
        yield l[i:i + k] 

# thread
        
def evolve_thread(parents, island_id, queue):
    prompt = getprompt(parents, island_id)
    response = callLLM(prompt)
    program = parse_response(response)
    queue.put(program)

# evolve with multithreading

def evolve(island, island_id):
    random.shuffle(island)
    splitlist = splitlist(island, k)
    splitlist_by_maxthread = splitlist(splitlist, max_threads_per_island)
    for run in splitlist_by_maxthread:
        queue = queue.Queue()
        pool = []
        for parents in run:
            thread = threading.Thread(target = evolve_thread, args = [parents, island_id, queue])
            pool.append(thread)
        for thread in pool:
            thread.start()
            response = queue.get()
            yield response
        for thread in pool:
            thread.join()