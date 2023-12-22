import random
from program_manager import readprogram
# put code for evaluator here
def evaluate(ids = None, program = None, island_id = None):
    if program == None:
        program = readprogram(ids, island_id)
    score = [random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]
    return score
