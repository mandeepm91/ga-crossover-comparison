from implementations.one_point_crossover import run_one_max_problem_with_1_point_crossover
from implementations.two_point_crossover import run_one_max_problem_with_2_point_crossover
from implementations.uniform_crossover import run_one_max_problem_with_uniform_crossover
from implementations.adaptive_crossover_random import run_one_max_problem_with_random_adaptive_crossover
from implementations.intelligent_adaptive_crossover import run_one_max_problem_with_intelligent_adaptive_crossover
from deap import creator, base
from db import save_execution_log_one_max, get_existing_entry_for_input_one_max
import time

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
    '2': {
        'name': 'Two point crossover',
        'runner': run_one_max_problem_with_2_point_crossover
    },
    '3': {
        'name': 'Uniform crossover',
        'runner': run_one_max_problem_with_uniform_crossover
    },
    '4': {
        'name': 'Random Adaptive Crossover',
        'runner': run_one_max_problem_with_random_adaptive_crossover
    },
    '5': {
        'name': 'Intelligent Adaptive Crossover',
        'runner': run_one_max_problem_with_intelligent_adaptive_crossover
    }
}


if __name__ == "__main__":
    for i in range(1, 11):
        for (operator_number, operator_details) in operator_number_to_name_map.items():
            problem_size = 100 * i
            for iteration_number in range(25):
                print("problem_size: {}".format(problem_size))
                print("operator: {}".format(operator_details['name']))
                print("iteration number: {}".format(iteration_number))
                start_time = int(round(time.time() * 1000))
                fitness_function = evalFitness
                max_fitness_function_calls = 200 * problem_size

                runner_function = operator_number_to_name_map[operator_number]['runner']

                existing_entry = get_existing_entry_for_input_one_max(
                    operator_name=operator_details['name'],
                    problem_size=problem_size,
                    iteration_number=iteration_number
                )

                if not existing_entry:
                    best_chromosome, logbook = runner_function(
                        problem_size=problem_size,
                        fitness_function=fitness_function,
                        max_fitness_function_calls=max_fitness_function_calls
                    )

                    best_chromosome_fitness = fitness_function(best_chromosome)[0]
                    # calculate time taken
                    # update each runner function to return the logbook
                    # store results in DB
                    print('---------------------------------------------------------')
                    print('---------------------------------------------------------')
                    end_time = int(round(time.time() * 1000))
                    time_in_milliseconds = end_time - start_time
                    save_execution_log_one_max(
                        operator_name=operator_details['name'],
                        problem_size=problem_size,
                        iteration_number=iteration_number,
                        time_in_milliseconds=time_in_milliseconds,
                        logbook=logbook,
                        best_chromosome=best_chromosome,
                        best_chromosome_fitness=best_chromosome_fitness
                    )
                else:
                    print('Already executed for the given input')

