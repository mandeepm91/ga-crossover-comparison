import psycopg
import json
import csv
from psycopg.rows import dict_row
from itertools import groupby
from operator import itemgetter

from pprint import pprint


def save_aggregate_results():
    # Connect to an existing database
    with psycopg.connect(
        "host=0.0.0.0 dbname=ga_crossover_comparison user=postgres password=postgres",
        row_factory=dict_row
    ) as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            # Execute a command: this creates a new table
            cur.execute("""
                select number_of_weights
                    ,operator_name
                    ,avg(time_in_milliseconds)::integer avg_time
                    ,avg(best_chromosome_fitness)::integer avg_best_fitness
                from execution_logs_scales
                where number_of_weights <= 1000
                group by 1,2
                order by 1,4
            """)

            result = cur.fetchall()
            # print(json.dumps(result))
    keys = result[0].keys()
    with open('aggregates.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(result)


def calculate_convergence_point(logbook):
    last_entry = logbook[-1]
    min_fitness = int(last_entry['min'])
    convergence_point = last_entry['gen']
    for gen in logbook:
        min_fitness_in_gen = int(gen['min'])
        if min_fitness_in_gen == min_fitness:
            convergence_point = gen['gen']
            break
    return convergence_point


def compute_avg_point_of_convergence(list_of_logbooks):
    points_of_convergence = []
    for logbook in list_of_logbooks:
        convergence_point = calculate_convergence_point(logbook)
        points_of_convergence.append(convergence_point)
    return sum(points_of_convergence)/len(points_of_convergence)

def save_all_results():
    # Connect to an existing database
    with psycopg.connect(
        "host=0.0.0.0 dbname=ga_crossover_comparison user=postgres password=postgres",
        row_factory=dict_row
    ) as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            # Execute a command: this creates a new table
            cur.execute("""
                select number_of_weights
                    ,operator_name
                    ,avg(time_in_milliseconds)::integer avg_time
                    ,avg(best_chromosome_fitness)::integer avg_best_fitness
                    ,jsonb_agg(logbook) as logbook_records
                from execution_logs
                where number_of_weights <= 1000
                group by 1,2
                order by 1,2
            """)

            result = cur.fetchall()

    for record in result:
        # each record has number_of_weights, operator_name,
        # avg_time, avg_best_fitness and a list of lists of objects as logbook_records
        # we need to compute the avg_iterations_till_convergence
        # first get the min fitness of the last row
        # then get the generation number where that min fitness was reached
        # do this for all logbooks of a operator, weights combo and get avg
        avg_point_of_convergence = compute_avg_point_of_convergence(record['logbook_records'])
        del record['logbook_records']
        record['avg_point_of_convergence'] = avg_point_of_convergence

    keys = result[0].keys()
    with open('aggregates_v2.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(result)


def get_denormalized_results():
    with psycopg.connect(
        "host=0.0.0.0 dbname=ga_crossover_comparison user=postgres password=postgres",
        row_factory=dict_row
    ) as conn:

        with open('denormalized_data.csv', 'w', newline='') as output_file:

        # Open a cursor to perform database operations
            with conn.cursor() as cur:
                keys = [
                    'operator_name',
                    'number_of_weights',
                    'iteration_number',
                    'max_fitness_function_calls',
                    'time_in_milliseconds',
                    'best_chromosome_fitness',
                    'avg',
                    'gen',
                    'max',
                    'min',
                    'std',
                    'nevals',
                    'crossover_operator'
                ]
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                # Execute a command: this creates a new table
                cur.execute("""
                    select operator_name
                        , number_of_weights
                        , iteration_number
                        , max_fitness_function_calls
                        , logbook
                        , time_in_milliseconds
                        , best_chromosome_fitness
                    from execution_logs_scales
                """)
                count = 0
                for record in cur:
                    for log_entry in record['logbook']:
                        denormalized_row = {
                            'operator_name': record['operator_name'],
                            'number_of_weights': record['number_of_weights'],
                            'iteration_number': record['iteration_number'],
                            'max_fitness_function_calls': record['max_fitness_function_calls'],
                            'time_in_milliseconds': record['time_in_milliseconds'],
                            'best_chromosome_fitness': record['best_chromosome_fitness'],
                            'avg': log_entry['avg'],
                            'gen': log_entry['gen'],
                            'max': log_entry['max'],
                            'min': log_entry['min'],
                            'std': log_entry['std'],
                            'nevals': log_entry['nevals'],
                            'crossover_operator': log_entry.get('crossover_operator'),
                        }
                        count += 1
                        dict_writer.writerow(denormalized_row)
                        if (count % 1000) == 0:
                            print(count)


def flatten(l):
    return [item for sublist in l for item in sublist]

def get_aggregates_v2(table_name="execution_logs_scales"):
    field_name = "number_of_weights"
    if table_name == "execution_logs_scales":
        field_name = "number_of_weights"
    else:
        field_name = "problem_size"
    with psycopg.connect(
        "host=0.0.0.0 dbname=ga_crossover_comparison user=postgres password=postgres",
        row_factory=dict_row
    ) as conn:

        with open('aggregates_v2_{}.csv'.format(table_name), 'w', newline='') as output_file:

        # Open a cursor to perform database operations
            with conn.cursor() as cur:
                keys = [
                    'operator_name',
                    field_name,
                    'avg_time',
                    'avg_best_fitness',
                    'avg',
                    'gen',
                    'max',
                    'min',
                    'std',
                    'nevals',
                ]
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                # Execute a command: this creates a new table
                cur.execute("""
                    select {}
                        , operator_name
                        , json_agg(logbook) as logbooks
                        , avg(time_in_milliseconds) as avg_time
                        , avg(best_chromosome_fitness) as avg_best_fitness
                    from {}
                    group by 1,2
                """.format(field_name, table_name))
                count = 0
                for record in cur:
                    flattened_logbook_entries = flatten(record.get('logbooks'))
                    grouper = itemgetter("gen")
                    logbook_of_averages = []
                    sorted_logbook_entries = sorted(flattened_logbook_entries, key = grouper)
                    for key, grp in groupby(sorted_logbook_entries, grouper):
                        grp = list(grp)
                        temp_dict = { "gen": key }
                        number_of_items = len(grp)
                        temp_dict["nevals"] = sum(item["nevals"] for item in grp) / number_of_items
                        temp_dict["avg"] = sum(item["avg"] for item in grp) / number_of_items
                        temp_dict["min"] = sum(item["min"] for item in grp) / number_of_items
                        temp_dict["max"] = sum(item["max"] for item in grp) / number_of_items
                        temp_dict["std"] = sum(item["std"] for item in grp) / number_of_items
                        logbook_of_averages.append(temp_dict)

                    for log_entry in logbook_of_averages:
                        denormalized_row = {
                            'operator_name': record['operator_name'],
                            field_name: record[field_name],
                            'avg_time': record['avg_time'],
                            'avg_best_fitness': record['avg_best_fitness'],
                            'avg': log_entry['avg'],
                            'gen': log_entry['gen'],
                            'max': log_entry['max'],
                            'min': log_entry['min'],
                            'std': log_entry['std'],
                            'nevals': log_entry['nevals']
                        }
                        count += 1
                        dict_writer.writerow(denormalized_row)
                        if (count % 1000) == 0:
                            print(count)


def get_stats_till_best_fitness(logbook, best_fitness):
    gen = 0
    nevals = 0
    for entry in logbook:
        gen = entry['gen']
        nevals += entry['nevals']
        if entry['min'] == best_fitness:
            break
    return gen, nevals

def get_average_for_metric(list_of_objects, metric_name):
    number_of_observations = len(list_of_objects)
    sum_of_observations = sum([entry[metric_name] for entry in list_of_objects])
    return (sum_of_observations * 1.0)/number_of_observations

def get_evals_till_best_fitness(table_name="execution_logs_scales"):
    field_name = "number_of_weights"
    if table_name == "execution_logs_scales":
        field_name = "number_of_weights"
    else:
        field_name = "problem_size"

    results = {}
    # Connect to an existing database
    with psycopg.connect(
        "host=0.0.0.0 dbname=ga_crossover_comparison user=postgres password=postgres",
        row_factory=dict_row
    ) as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            # Execute a command: this creates a new table
            cur.execute("""
                select *
                from {}
                where {} <= 1000
            """.format(table_name, field_name))

            for record in cur:
                operator_name = record['operator_name']
                if operator_name not in results:
                    results[operator_name] = {}
                problem_size = record[field_name]
                if problem_size not in results[operator_name]:
                    results[operator_name][problem_size] = []
                generation_till_best_fitness, nevals_till_best_fitness = get_stats_till_best_fitness(record['logbook'], record['best_chromosome_fitness'])
                stats = {
                    'generation_till_best_fitness': generation_till_best_fitness,
                    'nevals_till_best_fitness': nevals_till_best_fitness,
                    'best_fitness': record['best_chromosome_fitness']
                }
                results[operator_name][problem_size].append(stats)

    with open('evals_till_best_fitness_{}.csv'.format(table_name), 'w', newline='') as output_file:
        keys = [
            'operator_name',
            field_name,
            'avg_generations_till_best_fitness',
            'avg_nevals_till_best_fitness'
        ]
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        for operator_name, stats in results.items():
            for problem_size, list_of_entries in stats.items():
                avg_generations_till_best_fitness = get_average_for_metric(list_of_entries, 'generation_till_best_fitness')
                avg_nevals_till_best_fitness = get_average_for_metric(list_of_entries, 'nevals_till_best_fitness')
                row = {
                    'operator_name': operator_name,
                    field_name: problem_size,
                    'avg_generations_till_best_fitness': avg_generations_till_best_fitness,
                    'avg_nevals_till_best_fitness': avg_nevals_till_best_fitness
                }
                dict_writer.writerow(row)

# get_evals_till_best_fitness()
# get_aggregates_v2(table_name="execution_logs_one_max")
get_evals_till_best_fitness(table_name="execution_logs_one_max")