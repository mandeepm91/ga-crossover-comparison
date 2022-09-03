from deap import tools
import numpy
from .common import initialize_toolbox, eaSimpleRandomCrossover, initialize_toolbox_one_max
from .constants import POPULATION_SIZE, MAX_GENERATIONS, CROSSOVER_PROBABILITY, VERBOSE

def run_scales_problem_with_random_adaptive_crossover(
        weights = [],
        fitness_function = None,
        initial_population_size = POPULATION_SIZE,
        max_number_of_generations = MAX_GENERATIONS,
        max_fitness_function_calls = None
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

    size_of_chromosome = len(weights)
    mutation_rate = 1.0/size_of_chromosome

    result, log = eaSimpleRandomCrossover(
        pop, toolbox, cxpb=CROSSOVER_PROBABILITY, mutpb=mutation_rate,
        ngen=max_number_of_generations,
        verbose=VERBOSE,
        stats=stats,
        halloffame=hof,
        max_evals=max_fitness_function_calls
    )

    best_chromosome = tools.selBest(pop, k=1)
    print('Current best fitness:', fitness_function(best_chromosome[0]))
    print('best chromosome', best_chromosome)

    return best_chromosome[0], log


def run_one_max_problem_with_random_adaptive_crossover(
        problem_size = 0,
        fitness_function = None,
        initial_population_size = POPULATION_SIZE,
        max_number_of_generations = MAX_GENERATIONS,
        max_fitness_function_calls = None
    ):

    if not fitness_function:
        raise("FitnessFunctionNotDefined")

    toolbox = initialize_toolbox_one_max(problem_size, fitness_function)

    print('initial_population_size', initial_population_size)

    pop = toolbox.population(n=initial_population_size)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    size_of_chromosome = problem_size
    mutation_rate = 1.0/size_of_chromosome

    result, log = eaSimpleRandomCrossover(
        pop, toolbox, cxpb=CROSSOVER_PROBABILITY, mutpb=mutation_rate,
        ngen=max_number_of_generations,
        verbose=VERBOSE,
        stats=stats,
        halloffame=hof,
        max_evals=max_fitness_function_calls,
        maximization_problem=True
    )

    best_chromosome = tools.selBest(pop, k=1)
    print('Current best fitness:', fitness_function(best_chromosome[0]))
    print('best chromosome', best_chromosome)
    return best_chromosome[0], log
