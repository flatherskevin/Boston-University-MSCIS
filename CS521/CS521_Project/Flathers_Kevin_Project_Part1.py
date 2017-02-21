"""
Author: Kevin Flathers
Date Created: 02/09/2017
Date Last Edited: 02/19/2017
Course: CS521

The requirements for exactly what this file must do can be seen
in the attached files: CS521_Project_Part1.docx and CS521_Project_Part2.docx. Further explanation
as to what each class does is given within the respective class.
"""


import csv
import os
import sqlite3
import collections

class AbstractRecord:
    """
    Simple class that is inherited by other classes to use instance 'name'
    """
    name = ""


class StockStatRecord(AbstractRecord):
    """
    Inherits AbstractRecord class. Creates an object with properties of stock
    """

    def __init__(self, name, company_name, exchange_country, price, exchange_rate, shares_outstanding, net_income, market_value_usd, pe_ratio):
        """
        Constructor for StockStatsRecord

        :param name: stock ticker
        :param company_name: stock company name
        :param exchange_country: stock exchange country
        :param price: stock proce
        :param exchange_rate: stock rate
        :param shares_outstanding: stock shares outstanding
        :param net_income: stock net income
        :param market_value_usd: stock market value in USD
        :param pe_ratio: stock price / earnings ratio
        """
        self.name = name
        self.company_name = company_name
        self.exchange_country = exchange_country
        self.price = price
        self.exchange_rate = exchange_rate
        self.shares_outstanding = shares_outstanding
        self.net_income = net_income
        self.market_value_usd = market_value_usd
        self.pe_ratio = pe_ratio

    def __str__(self):
        """
        Re-write in accordance with Project guidelines

        :return: object string
        """
        return "{type}({name}, {company_name}, {exchange_country}, {price}, {exchange_rate}, {shares_outstanding}, {net_income}, {market_value_usd}, {pe_ratio})".format(type=self.__class__.__name__, name=self.name, company_name=self.company_name, exchange_country=self.exchange_country, price=round(self.price, 2), exchange_rate=round(self.exchange_rate, 2), shares_outstanding=round(self.shares_outstanding, 2), net_income=round(self.net_income, 2), market_value_usd=round(self.market_value_usd, 2), pe_ratio=round(self.pe_ratio, 2))


class BaseballStatRecord(AbstractRecord):
    """
    Inherits AbstractRecord class. Creates an object with properties of a baseball player
    """
    def __init__(self, name, salary, g, avg):
        """
        Constructor for BaseBallStatRecord class

        :param name: player name
        :param salary: player salary
        :param g: games played
        :param avg: batting average
        """
        self.name = name
        self.salary = salary
        self.g = g
        self.avg = avg

    def __str__(self):
        """
        Re-write in accordance with Project guidelines

        :return: object string
        """
        return "{type}({name}, {salary}, {g}, {avg})".format(type=self.__class__.__name__, name=self.name, salary=round(self.salary, 2), g=self.g, avg=round(self.avg, 2))


class AbstractCSVReader:
    """
    Generic CSV reader class
    """

    def __init__(self, path):
        """
        Constructor for AbstractCSVReader class

        :param path: path to CSV file, ./exampl/example.csv
        """

        # Ensure path exists
        try:
            if os.path.exists(path):
                self.path = path
            else:
                raise OSError("{path} does not exist".format(path=path))
        except OSError as err:
            print(err)
            self.path = "./"

    def row_to_record(self, row):
        """
        Generic method to be overwritten.

        :param row: contents from CSV row
        :return:
        """
        # Raise error if method has not been overwritten
        raise NotImplementedError

    def load(self):
        """
        Loads the data from the CSV (one row at a time), calls on row_to_record method to handle validation
        and parsing or each row, and passes valid rows, as dictionaries, to a list.

        :return: list of validated and parsed dictionaries from the rows of the CSV file
        """
        # Initialize a blank dictionary list to append validated rows to
        dictionary_list = []

        # Open the CSV file in read-only format
        with open(self.path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            # Establish the column headers
            header_row = next(csv_reader)

            # Loop through every row in the CSV file
            for row in csv_reader:

                # Initialize a blank dictionary for the row and a column counter
                row_dictionary = {}
                column = 0

                # Insert records into the dictionary with the corresponding header column being the key
                for item in row:
                    row_dictionary[header_row[column]] = item
                    column += 1

                # Begin error handling for bad data in the row
                try:
                    # Call on row_to_record to validate and parse the row
                    new_record = self.row_to_record(row_dictionary)

                    # If the record is returned as None, then the data was not valid and BadData error is raised
                    # Otherwise, append the validated and parsed row to the list of records
                    if not(new_record is None):
                        dictionary_list.append(new_record)
                    else:
                        raise BadData("Bad data in record")
                except BadData as err:
                    print(err)
                except NotImplementedError as err:
                    print(err)
        return dictionary_list


class BaseballCSVReader(AbstractCSVReader):
    """
    Class specifically for reading the baseball CSV. Inherits AbstractCSVReader class.
    """

    def row_to_record(self, row):
        """
        Overwrites row_to_record

        :param row: unvalidated an unparsed dictionary
        :return: validated and parsed record
        """
        # Establish what columns are important to look at
        important_keys = ['PLAYER', 'SALARY', 'G', 'AVG']

        # Initialize a clean dictionary to add validated and parsed data to
        return_row = {}

        # Loop through all important columns
        for key in important_keys:

            # Check that key column exists
            if key in row:

                # Check that key value is not blank
                if row[key] not in (None, ""):

                    # If the key is meant to be a string, add it to the dictionary
                    if key in 'PLAYER':
                        return_row[key] = row[key]

                    # If the key is meant to be a float, test that it can be converted
                    # into a numeric, round it two decimals, and add it to the dictionary
                    # Raise a BadData error if string cannot be converted
                    elif key in ('SALARY', 'G', 'AVG'):
                        try:
                            float(row[key])
                        except Exception as err:
                            raise BadData("{key} cannot convert to a float".format(key=row[key]))
                            return None
                        return_row[key] = round(float(row[key]), 2)
                else:
                    raise BadData("Empty cell in {key} column".format(key=key))
                    return None
            else:
                raise BadData("{key} column does not exist".format(key=key))
                return None

        # Return the dictionary as a record using BaseballStatRecord object
        return BaseballStatRecord(return_row['PLAYER'], return_row['SALARY'], return_row['G'], return_row['AVG'])


class StockCSVReader(AbstractCSVReader):
    """
    Class specifically for reading the stock CSV. Inherits AbstractCSVReader class.
    """

    def row_to_record(self, row):
        """
        Overwrites row_to_record

        :param row: unvalidated an unparsed dictionary
        :return: validated and parsed record
        """
        # Establish what columns are important to look at
        important_keys = ['ticker', 'company_name', 'exchange_country', 'price', 'exchange_rate', 'shares_outstanding', 'net_income', 'market_value_usd', 'pe_ratio']

        # Initialize a clean dictionary to add validated and parsed data to
        return_row = {}

        # Loop through all important columns
        for key in important_keys:

            # Check that key column exists
            if key in row:

                # Check that key value is not blank
                if row[key] not in (None, ""):

                    # If the key is meant to be a string, add it to the dictionary
                    if key in ('ticker', 'company_name', 'exchange_country'):
                        return_row[key] = row[key]

                    # If the key is meant to be a float, test that it can be converted
                    # into a numeric, round it two decimals, and add it to the dictionary
                    # Raise a BadData error if string cannot be converted
                    elif key in ('price', 'exchange_rate', 'shares_outstanding'):
                        try:
                            float(row[key])
                        except Exception:
                            raise BadData("{key} cannot convert to a float".format(key=row[key]))
                            return None
                        return_row[key] = round(float(row[key]), 2)

                    # If the key is meant to be a float, test that it can be converted
                    # into a numeric, round it two decimals, and add it to the dictionary
                    # Raise a BadData error if string cannot be converted or if net income is 0
                    elif key is 'net_income':
                        try:
                            float(row[key])
                        except Exception:
                            raise BadData("{key} cannot convert to a float".format(key=row[key]))
                        if row[key] is 0:
                            raise BadData("Net Income cannot be 0")
                        else:
                            return_row[key] = round(float(row[key]), 2)
                else:
                    raise BadData("Empty cell in {key} column".format(key=key))
                    return None

            # Calculate market_value_usd
            elif key is 'market_value_usd':
                market_value_usd = return_row['price'] * return_row['exchange_rate'] * return_row['shares_outstanding']
                return_row[key] = round(market_value_usd, 2)

            # Calculate pe_ratio
            elif key is 'pe_ratio':
                pe_ratio = return_row['price'] * return_row['shares_outstanding'] / return_row['net_income']
                return_row[key] = round(pe_ratio, 2)
            else:
                raise BadData("{key} column does not exist".format(key=key))
                return None

        # Return the dictionary as a record using StockStatRecord object
        return StockStatRecord(return_row['ticker'], return_row['company_name'], return_row['exchange_country'], return_row['price'], return_row['exchange_rate'], return_row['shares_outstanding'], return_row['net_income'], return_row['market_value_usd'], return_row['pe_ratio'])



class AbstractDAO:
    """
    Generic DAO class to be inherited
    """
    db_name = ""

    def insert_records(self, records):
        raise NotImplementedError

    def select_all(self):
        raise NotImplementedError

    def connect(self):
        return sqlite3.connect(self.db_name)


class BaseballStatsDAO(AbstractDAO):
    """
    DAO for baseball statistics
    """
    db_name = './baseball.db'

    def insert_records(self, records):
        current_db = self.connect()
        cursor = current_db.cursor()
        for record in records:
            cursor.execute("""
                INSERT INTO baseball_stats (player_name, salary, game_played, average)
                VALUES(?, ?, ?, ?)
            """, (record.name, record.salary, record.g, record.avg))
        current_db.commit()
        current_db.close()

    def select_all(self):
        current_db = self.connect()
        cursor = current_db.cursor()
        records = collections.deque()
        cursor.execute("""
            SELECT * FROM baseball_stats
        """)
        for record in cursor:
            records.append(BaseballStatRecord(record[0], record[3], record[1], record[2]))
        current_db.close()
        return records


class StocksDAO(AbstractDAO):
    """
    DAO for stocks
    """
    db_name = './stocks.db'

    def insert_records(self, records):
        current_db = self.connect()
        cursor = current_db.cursor()
        for record in records:
            cursor.execute("""
                INSERT INTO stock_stats (ticker, company_name, country, price, exchange_rate, shares_outstanding, net_income, market_value, pe_ratio)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (record.name, record.company_name, record.exchange_country, record.price, record.exchange_rate, record.shares_outstanding, record.net_income, record.market_value_usd, record.pe_ratio))
        current_db.commit()
        current_db.close()

    def select_all(self):
        current_db = self.connect()
        cursor = current_db.cursor()
        records = collections.deque()
        cursor.execute("""
            SELECT * FROM stock_stats
        """)
        for record in cursor:
            records.append(StockStatRecord(*record))
        current_db.close()
        return records


# Custom exception to handle record creation
class BadData(Exception):
    pass

print('\n<> <> <> <> <> <> <> <> <> <>')
print('\nRESULTS:  STOCKS\n')
print('<> <> <> <> <> <> <> <> <> <>\n')
# Loads all stock records into stocks.db
stocks_records = StockCSVReader('./StockValuations.csv')
stocks_DAO = StocksDAO()

try:
    stocks_DAO.insert_records(stocks_records.load())
except Exception as err:
    print(err)

all_stocks = stocks_DAO.select_all()
unique_exchange_country_list = []
exchange_country_tickers_dict = {}
for item in all_stocks:
    if item.exchange_country not in unique_exchange_country_list:
        unique_exchange_country_list.append(item.exchange_country)

for item in unique_exchange_country_list:
    count = 0
    for sub_item in all_stocks:
        if sub_item.exchange_country == item:
            count += 1
    exchange_country_tickers_dict[item] = count

for item in exchange_country_tickers_dict:
    print('{item} has {count} total tickers'.format(item=item, count=exchange_country_tickers_dict[item]))


print('\n<> <> <> <> <> <> <> <> <> <>')
print('\nRESULTS:  BASEBALL\n')
print('<> <> <> <> <> <> <> <> <> <>\n')


# Loads all baseball records into baseball.db
baseball_records = BaseballCSVReader('./MLB2008.csv')
baseball_DAO = BaseballStatsDAO()

try:
    baseball_DAO.insert_records(baseball_records.load())
except Exception as err:
    print(err)

all_baseball = baseball_DAO.select_all()
unique_avg_list = []
avg_salary_dict = {}
for item in all_baseball:
    if round(item.avg, 3) not in unique_avg_list:
        unique_avg_list.append(round(item.avg, 3))

for item in unique_avg_list:
    count = 0
    salary_sum = 0
    for sub_item in all_baseball:
        if sub_item.avg == item:
            count += 1
            salary_sum += sub_item.salary
    average_salary = salary_sum / count
    avg_salary_dict[item] = float(format(average_salary, '.2f'))

for item in avg_salary_dict:
    print('{item} batting average has and average salary of ${count}'.format(item=item, count=avg_salary_dict[item]))

