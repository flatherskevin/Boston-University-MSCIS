"""
Author: Kevin Flathers
Last Edited: 01/25/2017
Date Created: 01/25/2017
Course: CS521


The purpose of this file is to create a csv, insert in the csv file
integers 0 to 10 on separate lines (in a single column), read the csv
file, convert the values to integers, store the integers in a list,
and print the list to the console.
"""

import csv


def write_to_csv(filename, path=""):
    """
    Writes numbers 0 through 10 in a CSV file

    :param filename: name of csv file with .csv extension 'example.csv'
    :param path: *Optional* path to where the csv file exists '/example/'
    :return: None
    """

    with open(path + filename, 'w+') as csv_file:
        for number in range(11):
            csv.writer(csv_file).writerow([number])



def read_from_csv(filename, path=""):
    """
    Reads all rows of a csv file and returns each row, as an integer, in a list.

    The intent of this reader is to only be used on single entry, integer columns.

    :param filename: name of csv file with .csv extension 'example.csv'
    :param path: *Optional* path to where the csv file exists '/example/'
    :return: list containing integers from csv column
    """
    csv_list = []
    with open(path + filename, 'r') as csv_file:
        csv_read = csv.reader(csv_file)
        try:
            for row in csv_read:
                csv_list.append(int(*row))
        except ValueError as err:
            print(err)
    return csv_list

# Create the csv file
write_to_csv('test_file.csv')

# Read the created csv file and print it to the console
print(read_from_csv('test_file.csv'))
