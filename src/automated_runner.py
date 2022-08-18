from input_generator import get_first_n_primes
from implementations.one_point_crossover import run_scales_problem_with_1_point_crossover
from implementations.two_point_crossover import run_scales_problem_with_2_point_crossover
from implementations.uniform_crossover import run_scales_problem_with_uniform_crossover
from implementations.adaptive_crossover_random import run_scales_problem_with_random_adaptive_crossover
from implementations.intelligent_adaptive_crossover import run_scales_problem_with_intelligent_adaptive_crossover
from deap import creator, base
from implementations.common import get_fitness_function

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

operator_number_to_name_map = {
    '1': {
        'name': 'One point crossover',
        'runner': run_scales_problem_with_1_point_crossover
    },
    '2': {
        'name': 'Two point crossover',
        'runner': run_scales_problem_with_2_point_crossover
    },
    '3': {
        'name': 'Uniform crossover',
        'runner': run_scales_problem_with_uniform_crossover
    },
    '4': {
        'name': 'Random Adaptive Crossover',
        'runner': run_scales_problem_with_random_adaptive_crossover
    },
    '5': {
        'name': 'Intelligent Adaptive Crossover',
        'runner': run_scales_problem_with_intelligent_adaptive_crossover
    }
}

def display_weights(weights, best_chrosome):
    left_weights = []
    right_weights = []
    index = 0
    for bit in best_chromosome:
        if bit == 0:
            left_weights.append(weights[index])
        elif bit == 1:
            right_weights.append(weights[index])
        index += 1
    print('Left weights', left_weights, sum(left_weights))
    print('Right weights', right_weights, sum(right_weights))



if __name__ == "__main__":
    for (operator_number, operator_details) in operator_number_to_name_map.items():
        for i in range(1, 11):
            number_of_weights = 100 * i
            print("weights: {}".format(number_of_weights))
            print("operator: {}".format(operator_details['name']))
            weights = get_first_n_primes(int(number_of_weights))
            fitness_function = get_fitness_function(weights)
            runner_function = operator_number_to_name_map[operator_number]['runner']
            best_chromosome = runner_function(weights, fitness_function)
            display_weights(weights, best_chromosome)

# set mutation to 1/number of bits
# 1000 * number of weights max fitness function calls
# record the convergence point (the generation it reaches best fitness and does not change afterwards)

# keep varying it based on how close the convergence is to the starting generation vs last generation
# Helpful since you can justify the reasoning for setting up this value


