"""
Author: Kevin Flathers
Date Created: 02/14/2017
Date Last Edited: 02/20/2017
Course: CS521

File simply to create a stocks database and baseball database,
create tables within each.
"""

import sqlite3

# Path to the database
baseball_db_path = './baseball.db'

# Connect to the database
# Database will automatically be created if it does not exist
baseball_db = sqlite3.connect(baseball_db_path)

# Initialize a cursor
baseball_cursor = baseball_db.cursor()

# Create the table
baseball_cursor.execute("""
    CREATE TABLE IF NOT EXISTS baseball_stats(
        player_name TEXT PRIMARY KEY,
        game_played REAL,
        average REAL,
        salary REAL
    )
""")


# Path to the database
stocks_db_path = './stocks.db'

# Connect to the database
# Database will automatically be created if it does not exist
stocks_db = sqlite3.connect(stocks_db_path)

# Initialize a cursor
stocks_cursor = stocks_db.cursor()

# Create the table
stocks_cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_stats(
        company_name TEXT PRIMARY KEY,
        ticker TEXT,
        country TEXT,
        price REAL,
        exchange_rate REAL,
        shares_outstanding REAL,
        net_income REAL,
        market_value REAL,
        pe_ratio REAL
    )
""")
