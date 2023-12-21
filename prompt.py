from program_manager import readprogram

# EDIT THIS TO CHANGE PROMPT

def getprompt(ids: list):
    program = "generate a better program based on the following sample programs provided. The language is python."
    for program in ids:
        program_text = readprogram(program)
        program = program + "\n\n" + program_text
