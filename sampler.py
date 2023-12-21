import random, math
from settings import N, T_0, T_program
from program_manager import getprogramlength

"""
programs in islands are stored in the following format:
{"[a,b,c,d...]"(cluster):[program (highest score), ..., program (lowest score)]}
programs are stored based on IDs
"""
def sample(island: dict):

    # choosing cluster
    cluster_scores = {}
    total_programs = 0
    cluster_probabilities = []
    # get the score of the cluster
    for signature in list(island.keys()):
        total_programs = total_programs + 1
        cluster_score = sum(signature) / len(signature)
        cluster_scores[signature] = cluster_score
    index = 0
    # get probability of picking cluster
    for score in list(cluster_scores.values()):
        T_cluster = T_0 * (1 - (total_programs % N) / N)
        other_cluster_scores = list(cluster_scores.values).remove(score)
        for other_score in other_cluster_scores:
            denominator = denominator + math.exp(other_score / T_cluster)
        p = math.exp(score / T_cluster) / denominator
        cluster_probabilities.append(p)
        index = index + 1
    # pick cluster
    selected_signature = random.choices(list(island.keys()), cluster_probabilities)

    # choosing program
    # getting weight of program
    weights = []
    program_lengths = {}
    program_ids = island[selected_signature]
    for ids in program_ids:
        program_lengths[ids] = -getprogramlength(ids)
    for ids in program_ids:
        this_program_length = program_lengths[ids]
        other_program_lengths = program_lengths
        del program_lengths[ids]
        minlength = min(list(other_program_lengths.values()))
        maxlength = max(list(other_program_lengths.values()))
        weight = math.exp((this_program_length - minlength) / (maxlength + 00000.1) / T_program)
        weights.append(weight)
    selected_program_1 = random.choices(program_ids, weights)
    index_1 = program_ids.index(selected_program_1)
    del program_ids[index_1]
    del weights[index_1]
    selected_program_2 = random.choices(program_ids, weights)

    return [selected_program_1, selected_program_2]
