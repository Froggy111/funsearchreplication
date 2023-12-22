# funsearchreplication
not an exact replication of funsearch by google (mostly due to a skill issue)

USAGE INSTRUCTIONS:

Tweak settings in settings.py. *IMPORTANT* make sure that your computer / API provider is able to handle the number of threads

Name all of your init_programs as some number.py from 1, 2, 3, ... Make sure that the number of initial programs you have is larger than the value of k.

Run main.py to start evolving, to stop safely type stop in stop.txt and save, it will stop when the current iteration ends

Can add multithreading for score evaluation (shouldnt be an issue though)

Need to add actual API and actual evaluator and response parser (depends on the problem)