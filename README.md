# Word Count Tracker

## Description

A simple terminal app written in python to help the user keep track of
the number of words  they write, allowing them to create entries in
a PostgreSQL database containing a word count, a date, and optionally a
project title associated with the entry 
> Entry #: 1038  | Wordcount: 130  | Date: 2002-01-01  | 
> Project Title: Example

The user can then delete these entries or print them to the terminal screen
in the above format. 

## Usage: 

This program requires a PostgreSQL server with the word_count_entry table. 
This table can be found in the word_count_schema file. 

Once created, the program requires an INI file titled "database.ini" to
connect to this database. It must be in the same directory as the rest
of the program, have a section called [postgresql_conn_data], and 
have enough information to establish a connection to a PostgreSQL 
database (At a minimum, the name of the database. Host and port will 
default to localhost and 5432 respectively)
Example contents of such an INI file: 
    
    [postgresql_conn_data]
    host=localhost
    port=5432
    dbname=postgres
    user=example
    password=example1

With a server and an INI file to connect to it, the program can then be run
with "./main.py". All user input is given as command line arguments. The 
user must specify a command, either add, print or delete, and then supply the 
command line arguments each command requires, listed bwlow

- add:
    - --wordcount: Required, the wordcount of the entry to be added
    - --date: The date of the entry to be added. If the date is not supplied
    then it will default to the current day
    - --project: The name of the project associated with the entry. Is NULL if 
    not supplied

- delete: One of the following arguments is required
    - --id: Deletes the entry with the specified id
    - --all: Deletes all entries
    - --dates: Requires two dates, deletes all entries whose dates fall on or 
    between the two given datesdates.
    - --project: Deletes all entries associated with the specified project
- print
    - --all: Prints all entries
    - --dates: Requires two dates, prints all entries whose dates fall on or 
    between the two given dates
    - --project: Prints all entries associated with the specified project




## Goals:

I wanted to create a simple program that would involve connecting to
and querying a relational database. 

## Things to Add:

1. Slightly more complex queries 
(Exs: Avg number of words written per week & month)

2. Being able to process a pdf or plain text file and automatically create
a corresponding entry
       

## Acknowledgements:

The article "Connect to PostgreSQL Database Server Using Python Module 
of psycopg2" by Audhi Aprilliant for help with parsing INI files