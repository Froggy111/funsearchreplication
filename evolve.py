from api import callLLM
from prompt import getprompt
from settings import k
from parse_response import parse_response
import random
def splitlist(l): 
    for i in range(0, len(l), k):  
        yield l[i:i + k] 
def evolve(island):
    random.shuffle(island)
    splitlist = splitlist(island)
    for group in splitlist:
        prompt = getprompt(group)
        response = callLLM(prompt)
        program = parse_response(response)
        yield program        