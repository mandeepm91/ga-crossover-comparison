import psycopg

def create_execution_logs_scales_problem():
    # Connect to an existing database
    with psycopg.connect("host=0.0.0.0 dbname=ga_crossover_comparison user=postgres password=postgres") as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            # DROP TABLE
            cur.execute("DROP TABLE IF EXISTS execution_logs_scales")

            # Execute a command: this creates a new table
            cur.execute("""
                CREATE TABLE execution_logs_scales (
                    operator_name varchar(255),
                    number_of_weights integer,
                    iteration_number integer,
                    max_fitness_function_calls integer,
                    logbook jsonb,
                    time_in_milliseconds bigint,
                    best_chromosome jsonb,
                    best_chromosome_fitness bigint,
                    primary key (operator_name, number_of_weights, iteration_number)
                )
            """)

            # Make the changes to the database persistent
            conn.commit()

def create_execution_logs_one_max_problem():
    # Connect to an existing database
    with psycopg.connect("host=0.0.0.0 dbname=ga_crossover_comparison user=postgres password=postgres") as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            # DROP TABLE
            cur.execute("DROP TABLE IF EXISTS execution_logs_one_max")

            # Execute a command: this creates a new table
            cur.execute("""
                CREATE TABLE execution_logs_one_max (
                    operator_name varchar(255),
                    problem_size integer,
                    iteration_number integer,
                    logbook jsonb,
                    time_in_milliseconds bigint,
                    best_chromosome jsonb,
                    best_chromosome_fitness bigint,
                    primary key (operator_name, problem_size, iteration_number)
                )
            """)

            # Make the changes to the database persistent
            conn.commit()

def create_execution_logs_knapsack_problem():
    # Connect to an existing database
    with psycopg.connect("host=0.0.0.0 dbname=ga_crossover_comparison user=postgres password=postgres") as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            # DROP TABLE
            cur.execute("DROP TABLE IF EXISTS execution_logs_knapsack")

            # Execute a command: this creates a new table
            cur.execute("""
                CREATE TABLE execution_logs_knapsack (
                    operator_name varchar(255),
                    number_of_items integer,
                    iteration_number integer,
                    logbook jsonb,
                    time_in_milliseconds bigint,
                    best_chromosome jsonb,
                    best_chromosome_fitness bigint,
                    primary key (operator_name, number_of_weights, iteration_number)
                )
            """)

            # Make the changes to the database persistent
            conn.commit()


create_execution_logs_one_max_problem()