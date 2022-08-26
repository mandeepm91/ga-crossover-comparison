from sys import stderr
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

def get_aggregates_v2():
    with psycopg.connect(
        "host=0.0.0.0 dbname=ga_crossover_comparison user=postgres password=postgres",
        row_factory=dict_row
    ) as conn:

        with open('aggregates_v2.csv', 'w', newline='') as output_file:

        # Open a cursor to perform database operations
            with conn.cursor() as cur:
                keys = [
                    'operator_name',
                    'number_of_weights',
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
                    select number_of_weights
                        , operator_name
                        , json_agg(logbook) as logbooks
                        , avg(time_in_milliseconds) as avg_time
                        , avg(best_chromosome_fitness) as avg_best_fitness
                    from execution_logs_scales
                    group by 1,2
                """)
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
                            'number_of_weights': record['number_of_weights'],
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


get_aggregates_v2()