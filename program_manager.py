def getprogramlength(ids, island_id):
    with open(f"./programs/{island_id}/{ids}.py", "r") as f:
        length = len(f.read())
    return length
def readprogram(ids, island_id):
    return open(f"./programs/{island_id}/{ids}.py", "r").read()
def saveprogram(ids, program, island_id):
    with open(f"./programs/{island_id}/{ids}.py", "w") as f:
        f.write(program)