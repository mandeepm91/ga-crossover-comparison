from deap import tools
import numpy
from random import choice
from .common import eaSimpleIntelligentCrossover, initialize_toolbox


def run_scales_problem_with_intelligent_adaptive_crossover(
        weights = [],
        fitness_function = None,
        initial_population_size = 10,
        max_number_of_generations = 1000,
        max_fitness_function_calls = 1000
    ):

    if not fitness_function:
        raise("FitnessFunctionNotDefined")

    toolbox = initialize_toolbox(weights, fitness_function)

    pop = toolbox.population(n=initial_population_size)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    result, log = eaSimpleIntelligentCrossover(
        pop, toolbox, cxpb=0.5, mutpb=0.2,
        ngen=max_number_of_generations,
        verbose=True,
        stats=stats,
        halloffame=hof,
        max_evals=max_fitness_function_calls
    )

    best_chromosome = tools.selBest(pop, k=1)
    print('Current best fitness:', fitness_function(best_chromosome[0]))
    print('best chromosome', best_chromosome)

    return result, log

