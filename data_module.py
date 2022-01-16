import sys
import datetime
import psycopg2
from configparser import ConfigParser

class DataModule:   
    '''Connects to and handles querying an posgreSQL database

    Uses an INI file to establish a connection to a postgreSQL database
    containing the table word_count_entries and contains methods to query this  
    table. INI file must be titled "database.ini" with a section title of
    "postgresql_conn_data" and enough information for the psycopg2 connection 
    method to work (An example can be found in the README). 
    '''

    def __init__(self):
        '''
        Parses an INI file and established a connection to a POSTGRES
        database
        '''
        try: 
            config_parser = ConfigParser()
            config_parser.read("database.ini")

            config_params = config_parser.items("postgresql_conn_data")
            
            db_conn_dict = {}

            for config_param in config_params:
                key = config_param[0]
                value = config_param[1]
                db_conn_dict[key] = value

            self.conn = psycopg2.connect(**db_conn_dict)

            # Query the database so that an exception is raised if the
            # connection was unsuccessful
            cur = self.conn.cursor()
            cur.execute('SELECT * FROM word_count_entry')

        except psycopg2.Error: 
            sys.exit("There was a problem connecting to the database, please "
                     "ensure that there's a correctly formatted file named " 
                     "\"database.ini\" in the folder that this program is in")

    def __del__(self):
        self.conn.close()

    def add_entry(self, word_count, date, project_title):
        '''Adds a row with a word count, date, and project-title to a database

        Args:
            word_count: 
                integer greater than 0
            date: 
                Either a datetime object or a string representing
                valid date in yyyy-mm-dd format
            project_title: 
                An optional string of up to 100 characters
                representing the title of a project an entry is
                associated with
        '''
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO word_count_entry (word_count," \
                        "date_of_entry, project_title) VALUES (%s, %s, %s)",  
                        (word_count, date, project_title,))
            self.conn.commit()
            cur.close()
        except psycopg2.Error:
            self.conn.commit()
            cur.close()

            # A valid argument for the date paramater may either be a datetime
            # object or a string reprenting the date in y-m-d format. This
            # conversion ensures that if it's a datetime object, it will be
            # in y-m-d format without hours and seconds
            if type(date) is datetime.datetime:
                date = date.date()
            
            print("There was a problem adding this entry, which had a "
                  "word count of \"{}\", a date of \"{}\", and a project title "
                  "of \"{}\"".format(word_count, date, project_title))

    def delete_entry(self, entry_id):
        '''Deletes the entry with the specified id

        Args:
            entry_id:
                An integer corresponding to the unique, primary key of an entry
        '''
        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM word_count_entry WHERE id = %s",  
                        (entry_id,))
            self.conn.commit()
            cur.close()
        except psycopg2.Error: 
            self.conn.commit()
            cur.close()
            print("There was a problem deleting an entry with the id \"{}\" "
                  "from the database. Entry id's can can be checked with the "
                  "print command".format(entry_id))

    def delete_entries_in_date_range(self, first_date, second_date):
        '''Deletes the entries whose date's are in-between the given dates 
         (inclusive)

        Args:
            first_date:
                Either a datetime object or a string representing
                valid date in yyyy-mm-dd format, the first, earliest date in
                range to delete entries in
            second_date:
                Either a datetime object or a string representing
                valid date in yyyy-mm-dd format, the second, latest date in
                range to delete entries in
        '''
        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM word_count_entry WHERE date_of_entry >= " \
                        "%s AND date_of_entry <= %s", (first_date, 
                                                       second_date,))
            self.conn.commit()
            cur.close()
        except psycopg2.Error:
            self.conn.commit()
            cur.close()
            print("There was a problem deleting the entries in the date range "
                  "\"{}\" to \"{}\" from the database".format(first_date, 
                                                              second_date))

    def delete_all_entries(self):
        '''Deletes all entries in the word_count_entry table'''
        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM word_count_entry")
            self.conn.commit()
            cur.close()
        except psycopg2.Error:
            self.conn.commit()
            cur.close()
            print("There was a problem deleting all the database's entries")

    def delete_project_entries(self, project_title):
        '''Deletes the entries associated with a specific project

        Args:
            project_title:
                A string representing the title of the project whose entries 
                will be deleted
        '''
        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM word_count_entry WHERE project_title = %s",
                        (project_title,))
            self.conn.commit()
            cur.close()
        except psycopg2.Error: 
            self.conn.commit()
            cur.close()
            print("There was a problem deleting the entries for the project",
                  "\"{}\"".format(project_title))

    def select_entries_in_date_range(self, first_date, second_date):
        '''Retrieves the entries whose date's are in-between the given dates 
         (inclusive)

        Args:
            first_date:
                Either a datetime object or a string representing
                valid date in yyyy-mm-dd format, the first, earliest date in
                range to retrieves entries in
            second_date:
                Either a datetime object or a string representing
                valid date in yyyy-mm-dd format, the second, latest date in
                range to retrieves entries in

        Returns:
            A list of entries whose dates are in the specified range
        '''
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM word_count_entry WHERE " \
                        "date_of_entry >= %s AND date_of_entry <= %s", 
                        (first_date, second_date,))
            entries = cur.fetchall()
            cur.close()
            return entries
        except psycopg2.Error:
            cur.close()
            print("There was a problem retrieving the entries in the date "
                  "range \"{}\" to \"{}\" from the database".format
                  (first_date, second_date))

    def select_all_entries(self):
        '''Deletes all entries in the word_count_entry table
        
        Returns:
            A list of all the rows/entries in the word_count_entry table
        '''
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM word_count_entry")
            entries = cur.fetchall()
            cur.close()
            return entries
        except psycopg2.Error:
            cur.close()
            print("There was a problem retrieving all the entries from "
                  "the database")


    def select_project_entries(self, project_title):
        '''Retrieves the entries associated with a specific project

        Args:
            project_title:
                A string representing the title of the project whose entries 
                will be retrieved
        
        Returns:
            A list of all the entries whose project_title matches the specified
            project entry
        '''
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM word_count_entry WHERE " \
                        "project_title = %s", (project_title,))
            entries = cur.fetchall()
            cur.close()
            return entries
        except psycopg2.Error: 
            cur.close()
            print("There was a problem retrieving the entries for the project",
                  "\"{}\"".format(project_title))