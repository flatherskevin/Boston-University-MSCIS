"""
Author: Kevin Flathers
Date Created: 02/09/2017
Date Last Edited: 02/13/2017
Course: CS521

The purpose of this file is to provide multiple classes that assist
in the reading, validating, parsing, and returning of data from CSV
files. The requirements for exactly what this file must do can be seen
in the attached file, CS521_Project_Part1.docx. Further explanation
as to what each class does is given within the respective class.
"""


import csv
import os

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
        self.price = round(price, 2)
        self.exchange_rate = round(exchange_rate, 2)
        self.shares_outstanding = round(shares_outstanding, 2)
        self.net_income = round(net_income, 2)
        self.market_value_usd = round(market_value_usd, 2)
        self.pe_ratio = round(pe_ratio, 2)

    def __str__(self):
        """
        Re-write in accordance with Project guidelines

        :return: object string
        """
        return "{type}({name}, {company_name}, {exchange_country}, {price}, {exchange_rate}, {shares_outstanding}, {net_income}, {market_value_usd}, {pe_ratio})".format(type=self.__class__.__name__, name=self.name, company_name=self.company_name, exchange_country=self.exchange_country, price=self.price, exchange_rate=self.exchange_rate, shares_outstanding=self.shares_outstanding, net_income=self.net_income, market_value_usd=self.market_value_usd, pe_ratio=self.pe_ratio)


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
        self.salary = round(salary, 2)
        self.g = g
        self.avg = round(avg, 2)

    def __str__(self):
        """
        Re-write in accordance with Project guidelines

        :return: object string
        """
        return "{type}({name}, {salary}, {g}, {avg})".format(type=self.__class__.__name__, name=self.name, salary=self.salary, g=self.g, avg=self.avg)


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

            # Begin error handling
            try:
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
                            return_row[key] = round(float(row[key]), 2)
                    else:
                        raise BadData("Empty cell in {key} column".format(key=key))
                else:
                    raise BadData("{key} column does not exist".format(key=key))
            except BadData as err:
                print(err)

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

            # Begin error handling
            try:

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
            except BadData as err:
                print(err)
                return None

        # Return the dictionary as a record using StockStatRecord object
        return StockStatRecord(return_row['ticker'], return_row['company_name'], return_row['exchange_country'], return_row['price'], return_row['exchange_rate'], return_row['shares_outstanding'], return_row['net_income'], return_row['market_value_usd'], return_row['pe_ratio'])


# Custom exception to handle record creation
class BadData(Exception):
    pass

# Print all stock records to the console
stocks = StockCSVReader('./StockValuations.csv')
for item in stocks.load():
    print(item)

print("\n<><><><><><><><><><><><><><><><><><><><><><><>\n")

# Print all stock records to the console
stocks = BaseballCSVReader('./MLB2008.csv')
for item in stocks.load():
    print(item)
