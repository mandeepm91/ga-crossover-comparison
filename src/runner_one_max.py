from input_generator import get_first_n_primes
from implementations.one_point_crossover import run_one_max_problem_with_1_point_crossover
# from implementations.two_point_crossover import run_scales_problem_with_2_point_crossover
# from implementations.uniform_crossover import run_scales_problem_with_uniform_crossover
# from implementations.adaptive_crossover_random import run_scales_problem_with_random_adaptive_crossover
# from implementations.intelligent_adaptive_crossover import run_scales_problem_with_intelligent_adaptive_crossover
from deap import creator, base

def evalFitness(individual):
    fitness = sum(individual)
    return (fitness, )

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

operator_number_to_name_map = {
    '1': {
        'name': 'One point crossover',
        'runner': run_one_max_problem_with_1_point_crossover
    },
    # '2': {
    #     'name': 'Two point crossover',
    #     'runner': run_scales_problem_with_2_point_crossover
    # },
    # '3': {
    #     'name': 'Uniform crossover',
    #     'runner': run_scales_problem_with_uniform_crossover
    # },
    # '4': {
    #     'name': 'Random Adaptive Crossover',
    #     'runner': run_scales_problem_with_random_adaptive_crossover
    # },
    # '5': {
    #     'name': 'Intelligent Adaptive Crossover',
    #     'runner': run_scales_problem_with_intelligent_adaptive_crossover
    # }
}

def display_result(best_chromosome):
    print('best_chromosome', best_chromosome)
    print('length of chromosome', len(best_chromosome))
    print('number of 1s', sum(best_chromosome))

if __name__ == "__main__":
    problem_size = input("Specify the size of chromosome: ")
    problem_size = int(problem_size)
    print("Select from one of the crossover operators below:")
    for (operator_number, details) in operator_number_to_name_map.items():
        print("{}: {}".format(operator_number, details['name']))
    crossover_operator = input("enter your choice: ")
    print("Inputs:")
    print("problem_size: {}".format(problem_size))
    print("operator: {}".format(operator_number_to_name_map[crossover_operator]['name']))
    max_fitness_function_calls = 1000 * problem_size
    fitness_function = evalFitness

    runner_function = operator_number_to_name_map[crossover_operator]['runner']
    best_chromosome, logbook = runner_function(
        problem_size=problem_size,
        fitness_function=fitness_function,
        max_fitness_function_calls=max_fitness_function_calls
    )

    print('best_chromosome', best_chromosome)

    display_result(best_chromosome)