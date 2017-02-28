"""
Author: Kevin Flathers
Date Created: 02/09/2017
Date Last Edited: 02/20/2017
Course: CS521

The requirements for exactly what this file must do can be seen
in the attached files: CS521_Project_Part1.docx and CS521_Project_Part2.docx. Further explanation
as to what each class does is given within the respective class.

For best implementation of the file, first delete stocks.db and baseball.db,
run create_dbs.py, and then run this file. That will result in the cleanest data insertion and return
"""


import csv
import os
import queue
import threading

stocks_rows = queue.Queue()
stocks_records = queue.Queue()

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
                        return_row[key] = float(row[key])

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
                            return_row[key] = float(row[key])
                else:
                    raise BadData("Empty cell in {key} column".format(key=key))
                    return None

            # Calculate market_value_usd
            elif key is 'market_value_usd':
                market_value_usd = return_row['price'] * return_row['exchange_rate'] * return_row['shares_outstanding']
                return_row[key] = market_value_usd

            # Calculate pe_ratio
            elif key is 'pe_ratio':
                pe_ratio = return_row['price'] * return_row['shares_outstanding'] / return_row['net_income']
                return_row[key] = pe_ratio
            else:
                raise BadData("{key} column does not exist".format(key=key))
                return None

        # Return the dictionary as a record using StockStatRecord object
        return StockStatRecord(return_row['ticker'], return_row['company_name'], return_row['exchange_country'], return_row['price'], return_row['exchange_rate'], return_row['shares_outstanding'], return_row['net_income'], return_row['market_value_usd'], return_row['pe_ratio'])


class Runnable:
    def __call__(self):
        while True:
            try:
                queue_item = stocks_rows.get(timeout=1)
                print("{worker_id} is working hard!!".format(worker_id=id(queue_item)))

                 # Call on row_to_record to validate and parse the row
                new_record = self.row_to_record(queue_item)

                # If the record is returned as None, then the data was not valid and BadData error is raised
                # Otherwise, append the validated and parsed row to the list of records
                if not(new_record is None):
                    stocks_records.put(item=new_record)
                else:
                    raise BadData("Bad data in record")

            except queue.Empty:
                break
            except BadData:
                pass

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
                        return_row[key] = float(row[key])

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
                            return_row[key] = float(row[key])
                else:
                    raise BadData("Empty cell in {key} column".format(key=key))
                    return None

            # Calculate market_value_usd
            elif key is 'market_value_usd':
                market_value_usd = return_row['price'] * return_row['exchange_rate'] * return_row['shares_outstanding']
                return_row[key] = market_value_usd

            # Calculate pe_ratio
            elif key is 'pe_ratio':
                pe_ratio = return_row['price'] * return_row['shares_outstanding'] / return_row['net_income']
                return_row[key] = pe_ratio
            else:
                raise BadData("{key} column does not exist".format(key=key))
                return None
        # Return the dictionary as a record using StockStatRecord object
        return StockStatRecord(return_row['ticker'], return_row['company_name'], return_row['exchange_country'], return_row['price'], return_row['exchange_rate'], return_row['shares_outstanding'], return_row['net_income'], return_row['market_value_usd'], return_row['pe_ratio'])


class FastStocksCSVReader:
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

    def load(self):
        """
        Loads the data from the CSV (one row at a time), calls on row_to_record method to handle validation
        and parsing or each row, and passes valid rows, as dictionaries, to a list.

        :return: list of validated and parsed dictionaries from the rows of the CSV file
        """

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
                stocks_rows.put(row_dictionary)

        threads = []

        for item in range(0, 4):
            new_thread = threading.Thread(target=Runnable())
            new_thread.start()
            threads.append(new_thread)

        for item in threads:
            item.join()

        dictionary_list = list(stocks_records.queue)

        return dictionary_list


# Custom exception to handle record creation
class BadData(Exception):
    pass


stock_record_list = FastStocksCSVReader('./StockValuations.csv').load()

for record in stock_record_list:
    print(record.__str__())
