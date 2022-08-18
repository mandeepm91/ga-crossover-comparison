import psycopg

# Connect to an existing database
with psycopg.connect("host=0.0.0.0 dbname=ga_crossover_comparison user=postgres password=postgres") as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:

        # DROP TABLE
        cur.execute("DROP TABLE IF EXISTS execution_logs")

        # Execute a command: this creates a new table
        cur.execute("""
            CREATE TABLE execution_logs (
                operator_name varchar(255),
                number_of_weights integer,
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