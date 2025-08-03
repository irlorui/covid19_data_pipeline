from pathlib import Path
import re
import pandas as pd
import numpy as np
from src.db_utils import Database
import logging
from psycopg2 import sql


def get_csv_files():
    """
    Returns a list with the filepaths of all CSV files found in the ./data folder
    """

    data_folder = Path(__file__).parent.parent / 'data'
    csv_files = list(data_folder.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {data_folder}")
    
    return csv_files


def normalize_name(name: str):
    """
    Normalize a string
        - Removes extension (if string is a filename)
        - Lowercase
        - Replace whitespaces and dashes (-) for underscores (_)
        - Removes any character that is not letter, number or underscore (_)
        - Makes sure it starts with a letter character
    
    Parameters:
        name: str. CSV file name.

    Return:
        norm_name: str. normalized name
    """
    if Path(name):
        norm_name = Path(name).stem 
    norm_name = norm_name.lower() 
    norm_name = re.sub(r'[\s\-]+', '_', norm_name) 
    norm_name = re.sub(r'[^\w]', '', norm_name)
    if not re.match(r'^[a-z_]', norm_name):
        norm_name = 't_' + norm_name  
    return norm_name


def map_dtype(dtype):

    """
    Maps the dtypes of a dataframe's column to the correct Postgres data type.
    """

    if pd.api.types.is_integer_dtype(dtype):
        return 'INTEGER'
    elif pd.api.types.is_float_dtype(dtype):
        return 'FLOAT'
    elif pd.api.types.is_bool_dtype(dtype):
        return 'BOOLEAN'
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return 'TIMESTAMP'
    else:
        return 'TEXT'


def create_table(conn, 
                 df: pd.DataFrame,
                 schema_name: str, 
                 table_name:str):
    
    """
    Creates a table in the database matching the columns listed in the dataframe.

    Parameters:
        - conn: connection to the database.
        - df: dataframe. Dataframe with the source data.
        - schema_name: str. Name for the schema where table should be created
        - table_name: str. Name for the table to be created in DB
    """ 

    columns = [
        sql.SQL("{} {}").format(
            sql.Identifier(normalize_name(col)),
            sql.SQL(map_dtype(dtype))
        )
        for col, dtype in df.dtypes.items()
    ]
    create_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
        sql.Identifier(schema_name, table_name),
        sql.SQL(', ').join(columns)
    )
    logging.info(create_query)

    with conn.cursor() as cursor:
        cursor.execute(create_query)
        conn.commit()
        logging.info(f'Table {table_name} created successfully!')


def insert_dataframe(conn, 
                     df: pd.DataFrame, 
                     schema_name: str, 
                     table_name: str, 
                     chunk_size: int = 1000):

    """
    Inserts data into the DB from a dataframe by chunks. 
    Columns are mapped to match postgres data types.

    Parameters:
        - conn: connection to the database.
        - df: dataframe. Dataframe with the source data.
        - schema_name: str. Name for the schema where table should be created
        - table_name: str. Name for the table to be created in DB
        - chunk_size: int. Defines the size of the chunk. 1000 by default
    """

    cols = list(df.columns)
    norm_cols = [normalize_name(col) for col in cols]
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        values = [tuple(None if pd.isna(x) else x for x in row) for row in chunk.values]

        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ").format(
            sql.Identifier(schema_name, table_name),
            sql.SQL(', ').join(map(sql.Identifier, norm_cols))
        )

        with conn.cursor() as cursor:
            try:
                args_str = b','.join(
                    cursor.mogrify(f"({','.join(['%s'] * len(cols))})", row)
                    for row in values
                )
                cursor.execute(insert_query.as_string(cursor) + args_str.decode('utf-8'))
                conn.commit()
                logging.info(f'Batch {i} inserted into {table_name} successfully!')
            except Exception as e:
                logging.info(f'Error inserting data in table {table_name}: {e}')


def test_extraction(conn, 
                    csv_path: str, 
                    schema_name: str, 
                    table_name: str):
    """
    Tests if the extraction was done correctly by comparing:
      - the number of rows in the DB table
      - the number of rows in the CSV file

    If this counts are not equal, an error is Raised.
    """
    # Get original file data
    with open(csv_path, 'r', encoding='utf-8') as f:
        csv_row_count = sum(1 for line in f) - 1  # do not consider header

    # Get inserted data stats
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) FROM {schema_name}.{table_name};")
        db_row_count = cursor.fetchone()[0]

    if db_row_count == csv_row_count:
        logging.info(f"Test OK for table {table_name}: {db_row_count} rows in DB  == {csv_row_count} rows in CSV original.")
    else:
        logging.info(f"Test FAILED for table {table_name}: {db_row_count} rows in DB != {csv_row_count} rows in CSV original.")
        raise Exception (f'Extraction Test failed for table {table_name}')


def load_raw_file(csv_file: str, 
                  conn, 
                  schema_name: str = 'raw'):

    """
    Load a single CSV file into the database

    Parameters:
        - csv_file: filepath for the CSV file to be extracted and loaded to the DB
        - conn: connection to the database.
        - schema_name: str. Name for the schema where extraction should write.
    """

    logging.info(f'Loading CSV file {csv_file}...')

    # Read CSV file into dataframe
    df = pd.read_csv(csv_file)
    df.replace({np.nan: None}, inplace=True)
    table_name = normalize_name(csv_file)

    # Load the source data in the database
    create_table(conn, df, schema_name, table_name)
    insert_dataframe(conn, df, schema_name, table_name)
    test_extraction(conn, csv_file, schema_name, table_name)


def extract_source_data():

    """
    Entry point for the Extraction. 
    Will extract and load in the DB all the CSV files in the /data folder
    """
    
    db = Database(dbname = 'clinical_trials',
                  user = 'etl',
                  password = 'etl',
                  host='postgres')
    conn = db.get_connection()

    csv_paths = get_csv_files()

    for csv_file in csv_paths:
        load_raw_file(csv_file, conn)
