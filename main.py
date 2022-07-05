#!/usr/bin/env python3
# Author: Sean Reilly
# Date: 7/05/2022
'''A program to help the user keep track of the number of words they write, 
   allowing them to add, delete, and print entries in a postgres database
   that contain wordcounts, the date those words were written and, optionally,
   a project they were written for
'''
import datetime
from data_module import DataModule
import argparse

def process_delete_command(data_module, cl_args):
    '''Calls appropriate data module function depending on command line input
    
    The user can delete all entries in the database, an entry with a specific
    id, entries that fall within a range of dates, or all entries associated
    with a specific project.

    Args:
        data_module:
            Handles querying posgreSQL database
        cl_args:
            Contains parsed command line arguments
    '''
    if cl_args.id is not None:
            data_module.delete_entry(cl_args.id)
    elif cl_args.dates is not None:
        dates = cl_args.dates
        data_module.delete_entries_in_date_range(dates[0], dates[1])
    elif cl_args.project is not None:
        data_module.delete_project_entries(cl_args.project)
    else:
        data_module.delete_all_entries()

def print_entries (entries):
    if isinstance(entries, list):
        for row in entries:
            print ("Entry #:", row[0], " | Wordcount:", row[1], " | Date:", 
                    row[2], " | Project Title:", row[3]) 

def process_print_command(data_module, cl_args):
    '''Calls appropriate data module function depending on command line input
    
    The user can print all entries in the database, entries that fall within a 
    range of dates, or all entries associated with a specific project. 

    Args:
        data_module:
            Handles querying posgreSQL database
        cl_args:
            Contains parsed command line arguments
    '''
    if cl_args.project is not None:
        print_entries(data_module.select_project_entries(cl_args.project))
    elif cl_args.dates is not None:
        dates = cl_args.dates
        print_entries(data_module.select_entries_in_date_range 
                        (dates[0], dates[1]))
    else:
        print_entries(data_module.select_all_entries())

def main ():
    '''Proccesses command-line arguments, calling appropriate helper functions
       for different commands
    '''
    db = DataModule()

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help', dest="command")
    subparsers.required = True
    
    add_parser = subparsers.add_parser('add', help='Add a wordcount entry to the database')
    add_parser.add_argument('--wordcount', type=int, required=True, help='The wordcount of the entry to be added')
    add_parser.add_argument("--date", default=datetime.datetime.today(),  help='The date of the entry to be added')
    add_parser.add_argument('--project', help='The name of the project that\'s associated with the entry')

    print_parser = subparsers.add_parser('print', help='Prints entries in the database')
    print_group = print_parser.add_mutually_exclusive_group(required=True)
    print_group.add_argument("--all", action='store_true', help="Prints all entries")
    print_group.add_argument("--dates", nargs=2, help="Prints all entries between two dates")
    print_group.add_argument('--project', help='Prints all entries associated with a project')

    delete_parser = subparsers.add_parser('delete', help='Prints entries in the database')
    delete_group = delete_parser.add_mutually_exclusive_group(required=True)
    delete_group.add_argument("--id", type=int, help="Deletes the entry with the specified id")
    delete_group.add_argument("--all", action='store_true', help="Deletes all entries")
    delete_group.add_argument("--dates", nargs=2, help="Deletes all entries between two dates")
    delete_group.add_argument('--project', help='Deletes all entries associated with a project')

    args = parser.parse_args()
    if args.command == "add":
        db.add_entry(args.wordcount, args.date, args.project)
    elif args.command == "print":
        process_print_command(db, args)
    elif args.command == "delete":
        process_delete_command(db, args)

if __name__ == "__main__":
    main()