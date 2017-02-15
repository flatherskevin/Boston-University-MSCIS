'''
Author: Kevin Flathers
Last Edited: 01/30/2017
Date Created: 01/26/2017
Course: CS521

This program is built from a skeleton provided from the instructor.
The goal is to read in a noun, verb, and adjective list from separate files,
and shuffle them at the start if the program. Then, the user is asked for
their username. A saved game file will be created if that user does not exist.
If a user uses a previously added username, the old game will be resumed. The
game will load any old data to be used during the current game. The user will
be asked to enter a number within a boundary, and random indices from the previous
three lists will replace 'noun', 'verb', and 'adjective', respectively, in a random sentence
brought in from a file with the resources folder. The user will be notified if the
sentence has already been created, otherwise it will be added to their saved games,
and their saved games will be printed back to them. Lastly, the user will be
asked to continue or end the program. If the user chooses to continue, everything
will be repeat a sequential time.
'''

import csv
import os
import random
import sys

def load_csv_to_list(path_to_file):
    """
    Reads a csv file and returns each row as a node in a list

    :param path_to_file: path the csv file 'Example/example.csv'
    :return: list where each node is a row from the csv
    """

    # Validate Path to file exists
    if not os.path.exists(path_to_file):
        print("""The file %s does not exist.
        That file will be created now...""" % path_to_file)

    # Validate file exists
    csv_list = []

    # Do not use csv library for reading lists in, sentences with a comma will break
    with open(path_to_file, 'r') as csv_file:

        # read().splitlines() is the remedy for commas in sentences
        csv_read = csv_file.read().splitlines()
        try:
            for row in csv_read:
                if row:
                    csv_list.append(row)
        except ValueError as err:
            print(err)

    # Return a list of items from file
    return csv_list

def shuffle(sequence):
    """
    Returns a shuffled list

    :param sequence: list to shuffle
    :return: shuffled list
    """
    shuffled_sequence = []
    while len(sequence):
        item_to_pop = int(random.random() * len(sequence))
        shuffled_sequence.append(sequence.pop(item_to_pop))
    return shuffled_sequence



def load_mad_lib_resource(path_to_resource):
    """
    Calls on load_csv_to_list(), verifies the file exists, shuffles
    the list, and, finally, returns the shuffled list as a tuple

    :param path_to_resource: path the csv file 'Example/example.csv'
    :return: shuffled list from csv as a tuple
    """

    # Call load_csv_to_list
    resource_list = load_csv_to_list(path_to_resource)

    # Verify the file exists and list is valid
    try:
        os.path.exists(path_to_resource)
        try:
            shuffled_resource_list = shuffle(resource_list)
            if "" in shuffled_resource_list:
                raise ValueError("Blank nodes exist in the list")

            # Return a tuple of the shuffled list
            return tuple(shuffled_resource_list)
        except ValueError as err:
            print(err)

            # Upon error, return a blank tuple
            return tuple()
    except IOError as err:
        print(err)

        # Upon error, return a blank tuple
        return tuple()




def play_game(user_sentences,lower_bound, upper_bound):
    is_keep_playing = None

    while is_keep_playing != 'n':
        user_str_number = input(
            "Please provide a number between {} and {}: ".format(lower_bound, upper_bound)
        )

        try:
            user_number = int(user_str_number.strip().lower())
        except:
            print("Sorry the value provided is not an integer.")
            user_number = None

        if user_number is not None:
            if user_number < MIN_VALUE:
                print("Sorry the number provided is too small (lower than {})".format(MIN_VALUE))
            elif user_number > MAX_VALUE:
                print("Sorry the number provided is too big (greater than {})".format(MAX_VALUE))
            else:
                sentence_idx = random.randint(user_number, MAX_VALUE) % len(SENTENCES)
                noun_idx = random.randint(user_number, MAX_VALUE) % len(NOUNS)
                verb_idx = random.randint(user_number, MAX_VALUE) % len(VERBS)
                adjective_idx = random.randint(user_number, MAX_VALUE) % len(ADJECTIVES)

                # generate the mad lib sentence
                sentence = SENTENCES[sentence_idx].format(
                    noun=NOUNS[noun_idx],
                    verb=VERBS[verb_idx],
                    adjective=ADJECTIVES[adjective_idx]
                )

                # GENERATE THE SENTENCES AND WRITE TO THE FILE IF NOT ALREADY SAVED
                # Initialize saved_games
                game_index = ''
                with open(os.path.join('resources', 'saved_games_%s.csv' % user_name), 'r') as saved_mad_libs:
                    reader = saved_mad_libs.readlines()

                    # Check if the sentence already exists
                    if sentence not in reader:

                        # Use indexID in string to allow for easier sorting method
                        # Unfortunately, the game can only support 99,999,999 games before breaking the sorting pattern
                        game_index = 'indexID{}'.format(len(reader))
                    else:
                        game_index = None
                        print("That sentence has already been created...")

                with open(os.path.join('resources', 'saved_games_%s.csv' % user_name), 'a+') as saved_mad_libs:
                    writer = csv.writer(saved_mad_libs)

                    if game_index != None:
                        # Make sure to force the sentence to be a string
                        writer.writerow([str(sentence), game_index])

                # PRINT ALL OF THE SENTENCES FOR THE USER THUS FAR
                # the previously used indexID provides a clear breaking point between sentence and sentence counter
                print("Your current, saved mad lib is...\n")

                # Before printing the current user created sentences, they must be loaded from the file again
                user_sentences = []
                with open(os.path.join('resources', 'saved_games_%s.csv' % user_name), 'r') as user_games:
                    # read().splitlines() is the remedy for commas in sentences
                    csv_read = user_games.read().splitlines()
                    try:
                        for row in csv_read:
                            if row:
                                user_sentences.append(row)
                    except ValueError as err:
                        print(err)

                # user_sentences is sorted by the number following the indexID text
                user_sentences = sorted(user_sentences, key=lambda x:x[-8:])
                for item in user_sentences:

                    # Now, we are able to use the indexID to easily print only the user sentence without the index
                    print(item[:item.find(',indexID')])

        is_keep_playing = None  # reset

        while 'y' != is_keep_playing and 'n' != is_keep_playing:
          is_keep_playing = input("\nDo you want to keep playing? (y / n): ")
          try:
            is_keep_playing = is_keep_playing.strip().lower()
          except:
            is_keep_playing = None

          if 'y' != is_keep_playing and 'n' != is_keep_playing:
            print("Sorry, I did not get that.")


# GET THE LISTS FROM THE FILES
ADJECTIVES = load_mad_lib_resource('resources/CS521_assignment2_adjectives.csv')
NOUNS = load_mad_lib_resource('resources/CS521_assignment2_nouns.csv')
SENTENCES = load_mad_lib_resource('resources/CS521_assignment2_sentences.csv')
VERBS = load_mad_lib_resource('resources/CS521_assignment2_verbs.csv')

#VERIFY THE LISTS EXIST

try:
    if not len(ADJECTIVES):
        raise ValueError("The ADJECTIVES tuple is empty")
    if not len(NOUNS):
        raise ValueError("The NOUNS tuple is empty")
    if not len(SENTENCES):
        raise ValueError("The SENTENCES tuple is empty")
    if not len(VERBS):
        raise ValueError("The VERBS tuple is empty")
except ValueError as err:
    print(err)
except Exception as err:
    print(err)

# boundaries
MIN_VALUE = 0
MAX_VALUE = max(
        len(SENTENCES),
        len(NOUNS),
        len(VERBS),
        len(ADJECTIVES),
)

# PROMPT FOR USERNAME
user_name = input("What is you username? ")

# VERIFY THE A USER NAME WAS ENTERED ELSE EXIT THE PROGRAM
try:
    if user_name is None or user_name is "":
        raise ValueError("A username was not provide. The program will now exit.")
except ValueError as err:
    print(err)
    sys.exit()

# FIND OUT IF THERE IS AN EXISTING USER SAVED GAMES

# user's mad lib
user_sentences = []

# GET THE USER'S SAVED GAMES IF IT EXISTS
if not os.path.exists(os.path.join('resources', 'saved_games_%s.csv' % user_name)):
    with open(os.path.join('resources', 'saved_games_%s.csv' % user_name), 'wb'):
        pass

with open(os.path.join('resources', 'saved_games_%s.csv' % user_name), 'r') as user_games:
    # read().splitlines() is the remedy for commas in sentences
    csv_read = user_games.read().splitlines()
    try:
        for row in csv_read:
            if row:
                user_sentences.append(row)
    except ValueError as err:
        print(err)

# SORT THE USER SENTENCES
# Use the sorted function within Python
# Since each line from the csv will come in as an entire string, begin searching from
# Unfortunately, the game can only support 99,999,999 games before breaking the sorting pattern
user_sentences = sorted(user_sentences, key=lambda x:x[-8:])

# CALL PLAY GAME FUNCTION
play_game(user_sentences, MIN_VALUE, MAX_VALUE)

print("Bye!")
