"""
Author: Kevin Flathers
Date Created: 02/14/2017
Date Last Edited: 02/19/2017
Course: CS521
"""

import sqlite3


baseball_db_path = './baseball.db'

baseball_db = sqlite3.connect(baseball_db_path)

baseball_cursor = baseball_db.cursor()

baseball_cursor.execute("""
    CREATE TABLE IF NOT EXISTS baseball_stats(
        player_name TEXT PRIMARY KEY,
        game_played REAL,
        average REAL,
        salary REAL
    )
""")



stocks_db_path = './stocks.db'

stocks_db = sqlite3.connect(stocks_db_path)

stocks_cursor = stocks_db.cursor()

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
