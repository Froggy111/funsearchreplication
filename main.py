from evaluator import evaluate
from evolve import evolve
from sampler import sample
from settings import n

# initialise islands

all_islands = {}
for i in range(n):
    all_islands[i] = {}