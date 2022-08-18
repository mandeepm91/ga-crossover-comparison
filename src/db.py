import psycopg
import json

def get_existing_entry_for_input(operator_name, number_of_weights, iteration_number):
    with psycopg.connect("host=0.0.0.0 dbname=ga_crossover_comparison user=postgres password=postgres") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 1 FROM execution_logs
                WHERE operator_name = %s
                AND number_of_weights = %s
                AND iteration_number = %s
            """, (operator_name, number_of_weights, iteration_number))
            data = cur.fetchone()
            return data is not None

def save_execution_log(
        operator_name,
        number_of_weights,
        iteration_number,
        logbook,
        time_in_milliseconds,
        best_chromosome,
        best_chromosome_fitness
    ):
        with psycopg.connect("host=0.0.0.0 dbname=ga_crossover_comparison user=postgres password=postgres") as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO execution_logs (
                        operator_name,
                        number_of_weights,
                        iteration_number,
                        logbook,
                        time_in_milliseconds,
                        best_chromosome,
                        best_chromosome_fitness
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """,
                    (
                        operator_name,
                        number_of_weights,
                        iteration_number,
                        json.dumps(logbook),
                        time_in_milliseconds,
                        json.dumps(best_chromosome),
                        best_chromosome_fitness
                    )
                )