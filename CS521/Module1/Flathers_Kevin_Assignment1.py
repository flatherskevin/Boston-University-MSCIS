"""
Author: Kevin Flathers
Last Edited: 01/22/2017
Date Created: 01/17/2017
Course: CS521

The purpose of this program is to emulate a mad lib.
The user will input an integer that will be used
to assemble the mad lib sentence. The sentence will be saved to
a list of sentences if it is unique (not created before). Then,
the whole mad lib (all created sentences) will be printed to the
console. Lastly, the user will be prompted to continue (repeat) or exit.
Functions will provide proper error handling of
user integer input and for repeating the program.
"""


NOUNS = ["time", "year", "people", "way", "day", "man", "thing", "woman"]
VERBS = ["pay", "put", "read", "run", "say", "see"]
ADJECTIVES = ["other", "new", "good", "high", "old"]
SENTENCES = [
    "Man verb on a adjective noun.",
    "Noun verb to the adjective ground.",
    "All the king’s adjective horses and all the king’s dainty noun could not verb scrambled egg man back together again."
]


# There needs to be an empty list initialized that can hold the unique mad lib sentences
sentence_list = []


"""
Function that returns user input:
Argument 1: minimum length of all mad lib lists
Handles errors for not a positive integer and if integer is out of range
"""
def input_integer(min_length):
    while True:
        try:
            user_int = int(input("Please input a positive integer: "))
            if not 0 < user_int <= min_length:
                raise ValueError("This integer is out range!")
            break
        except ValueError as err:
            print(err)
    return user_int


"""
Function that checks for the shortest length of the mad lib lists
"""
def check_length(noun_list, verb_list, adj_list, sentence_list):
    return min(len(noun_list), len(verb_list), len(adj_list), len(sentence_list))


"""
Function that takes in the user input integer and the mad lib lists, and then
returns an array of values gathered from the mad lib list's indexes that matched the
user input integer. Since the user is inputting a positive integer, 1 must be subtracted
from it to allow for an index of 0
Return indexing is as follows:
0 => NOUNS
1 => VERBS
2 => ADJECTIVES
3 => SENTENCES
"""
def gather_selection(user_int, noun_list, verb_list, adj_list, sentence_list):
    data_list = [noun_list, verb_list, adj_list, sentence_list]
    selection_list = []
    i = 0
    while i < len(data_list):
        selection_list.append(data_list[i][user_int - 1])
        i += 1
    return selection_list


"""
Function that replaces 'noun', 'verb', and 'adjective' in the selected sentence with
the respective values from a return list from the function gather_selection.
Raises an error if the sentence has been created before. Otherwise, prints, then returns, the
created sentence.
"""
def create_sentence(selection_list):
    #Replace those in middle of sentence
    selection_list[3] = selection_list[3].replace("noun", selection_list[0])
    selection_list[3] = selection_list[3].replace("verb", selection_list[1])
    selection_list[3] = selection_list[3].replace("adjective", selection_list[2])

    #Replace those at beginning of sentence
    selection_list[3] = selection_list[3].replace("Noun", selection_list[0])
    selection_list[3] = selection_list[3].replace("Verb", selection_list[1])
    selection_list[3] = selection_list[3].replace("Adjective", selection_list[2])

    try:
        if selection_list[3] in sentence_list:
            raise ValueError("This sentence has already been used...")
        else:
            sentence_list.append(selection_list[3])
            return sentence_list[-1]
    except ValueError as err:
        print(err)


"""
Function that prints out the current mad lib.
Takes the current saved list of sentences as an argument
"""
def print_madlib(sentence_list):
    for sentence in sentence_list:
        print(sentence.capitalize())


"""
Function that asks user if they want to continue.
'y' returns True; 'n' returns False
"""
def input_continue():
    while True:
        try:
            user_continue = input("Would you like to continue (y/n)? ")
            if not (user_continue is "y" or user_continue is "n"):
                raise ValueError("I didn't understand that response.... try again")
            if user_continue is "y":
                return True
            elif user_continue is "n":
                return False
        except ValueError as err:
            print(err)


"""
Function that runs the program. Initiates all steps in proper order.
"""
def main_program():
    user_continue = True
    while user_continue:
        min_length = check_length(NOUNS, VERBS, ADJECTIVES, SENTENCES)
        user_int = input_integer(min_length)
        selection_list = gather_selection(user_int, NOUNS, VERBS, ADJECTIVES, SENTENCES)
        create_sentence(selection_list)
        print("Your current mad lib is:\n")
        print_madlib(sentence_list)
        print("\n")
        user_continue = input_continue()
        print("\n\n")


main_program()
