def getprogramlength(ids, island_id):
    with open(f"./programs/{island_id}/{ids}.py", "r") as f:
        length = len(f.read())
        f.close()
    return length
def readprogram(ids, island_id):
    with open(f"./programs/{island_id}/{ids}.py", "r") as f:
        program = f.read()
        f.close()
    return program
def saveprogram(ids, program, island_id):
    with open(f"./programs/{island_id}/{ids}.py", "w") as f:
        f.write(program)
        f.close()