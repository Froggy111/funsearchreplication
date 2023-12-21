def getprogramlength(ids):
    with open(f"./programs/{ids}.py", "r") as f:
        length = len(f.read())
    return length
def readprogram(ids):
    return open(f"./programs/{ids}.py", "r").read()