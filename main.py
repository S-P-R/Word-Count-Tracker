#!/usr/bin/env python3
# Author: Sean Reilly
# Date: 1/14/2022
'''A program to help the user keep track of the number of words they write, 
   allowing them to add, delete, and print entries in a postgres database
   that contain wordcounts, the date those words were written and, optionally,
   a project they were written for
'''
import datetime
from data_module import DataModule

def print_commands():
    '''Prints the commands available to the user of this program'''
    
    print("The following is a list of commands. [] indicates an optional "
          "part of a command. Anything in () should not be entered directly, "
          "but is instead a description of what sorts of values should be " 
          "entered or what the command does:\n\n"        
          "     help\n\n"
          "     add (positive integer representing wordcount) "
          "[(date in ISO format)] [(string representing the title of "
          "a project)]\n\n"
          "     delete (integer representing id of project, id's can be found "
          "with the print command)\n"
          "     delete dates (first date in range entries will be deleted in) " 
          "(second date in range entries will be deleted in)\n"
          "     delete project (name of project whose entries will be " 
          "deleted)\n\n"
          "     print all \n"
          "     print dates (first date in range entries will be printed in) " 
          "(second date in range entries will be printed in)\n"
          "     print project (name of project whose entries will be printed)\n"
          "\n     quit \n")

def parse_add_command(data_module, user_input):
    '''Parses user input for the add command
    
    The user can add an entry to the database by specifying a word count (in 
    this case current date is used), a word count and date, or a word count, 
    date, and project title. This function parses user input so that the
    correct one of these options can be fulfilled depending on user input.

    Args:
        user_input:
            A length 2 list of strings  representing user input from the
            command line, with the 0th index containing the string "add"
            and the 1st containing the rest of the command
    '''
    user_input = (" ".join(user_input)).split(None, 3)

    if len(user_input) == 1:
        print("Invalid command, adding an entry requires a wordcount")
    if len(user_input) == 2:
        data_module.add_entry(user_input[1], datetime.datetime.today(), None)
    if len(user_input) == 3:
        data_module.add_entry(user_input[1], user_input[2], None)
    if len(user_input) == 4:
        data_module.add_entry(user_input[1], user_input[2], user_input[3])

def parse_delete_command(data_module, user_input):
    '''Parses user input for the delete command
    
    The user can delete all entries in the database, an entry with a specific
    id, entries that fall within a range of dates, or all entries associated
    with a specific project. This function function parses user input so that 
    the correct one of these options can be fulfilled depending on user input

    Args:
        user_input:
            A length 2 list of strings  representing user input from the
            command line, with the 0th index containing the string "delete"
            and the 1st containing the rest of the command
    '''
    user_input = (" ".join(user_input)).split(None, 2)

    if len(user_input) == 1:
            print("Invalid command, specify which entries to remove")
    elif user_input[1] == "all":
        data_module.delete_all_entries()
    elif len(user_input) == 2:
        data_module.delete_entry(user_input[1])
    elif user_input[1] == "project":
        data_module.delete_project_entries(user_input[2])
    elif user_input[1] == "dates":
        # Resplit user input so dates can be processed
        user_input = (" ".join(user_input)).split(None, 3) 
        
        if len(user_input) < 4:
            print("This command requires two dates")
        else:
            data_module.delete_entries_in_date_range(user_input[2], 
                                                     user_input[3])
    else:
        print("Invalid command, \"{}\" is not a valid way of specifying " 
              "which entries to remove".format(user_input[1]))

def print_entries (entries):
    if isinstance(entries, list):
        for row in entries:
            print ("Entry #:", row[0], " | Wordcount:", row[1], " | Date:", 
                    row[2], " | Project Title:", row[3]) 

def parse_print_command(data_module, user_input):
    '''Parses user input for the print command
    
    The user can print all entries in the database, entries that fall within a 
    range of dates, or all entries associated with a specific project. This 
    function function parses user input so that the correct one of these 
    options can be fulfilled depending on user input

    Args:
        user_input:
            A length 2 list of strings  representing user input from the
            command line, with the 0th index containing the string "print"
            and the 1st containing the rest of the command
    '''
    user_input = (" ".join(user_input)).split(None, 2)

    if len(user_input) == 1:
        print("Invalid command, specify which entries to print")
    elif user_input[1] == "all":
        print_entries(data_module.select_all_entries())
    elif user_input[1] == "project":
        print_entries(data_module.select_project_entries(user_input[2]))
    elif user_input[1] == "dates":
        user_input = (" ".join(user_input)).split(None, 3) 
        if len(user_input) < 4:
            print("This command requires two dates")
        else:
            print_entries(data_module.select_entries_in_date_range 
                          (user_input[2], user_input[3]))
    else:
        print("Invalid command, \"{}\" is not a valid way of specifying " 
              "which entries to print".format(user_input[1]))

def main ():
    '''Takes user input until the user inputs "quit"'''
    db = DataModule()

    print("Enter help for a list of commands")
    end_program = False 
    while not end_program:
        user_input = input("Command: ").split(None, 1)

        if len(user_input) < 1:
            continue
        if user_input[0] == "help":
            print_commands()
        elif user_input[0] == "add":
           parse_add_command(db, user_input)
        elif user_input[0] == "delete":
            parse_delete_command(db, user_input)
        elif user_input[0] == "print":
            parse_print_command(db, user_input)
        elif user_input[0] == "quit":
            end_program = True
        else:
            print("Invalid command, enter help for a list of commands")

if __name__ == "__main__":
    main()