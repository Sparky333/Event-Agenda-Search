#!/usr/bin/env python3
import argparse
import os
import pandas as pd
from db_table import db_table
'''
TODO:
Add comments in code
Add Null or required attributes to table declarations?
'''

'''
    
    users.insert({"name": "Simon Ninon", "email": "simon.ninon@whova.com"})
    users.insert({"name": "Xinxin Jin", "email": "xinxin.jin@whova.com"})
    users.insert({"name": "Congming Chen", "email": "congming.chen@whova.com"})
    users.select()
    users.update({'name': 'John'}, {'id':2})
    users.select(['name', 'email'], {'id': 2})
'''    


def load_tables(df):
    sessions =              db_table("sessions", 
                                    {"sessionid": "integer PRIMARY KEY AUTOINCREMENT", 
                                    "date": "text", 
                                    "time_start": "text", 
                                    "time_end": "text", 
                                    "session_title": "text", 
                                    "location": "text", 
                                    "description": "text", 
                                    "speakers": "text"})
    subsessions =           db_table("subsessions", 
                                    {"subsessionid": "integer PRIMARY KEY AUTOINCREMENT", 
                                    "date": "text", 
                                    "time_start": "text", 
                                    "time_end": "text", 
                                    "session_title": "text", 
                                    "location": "text", 
                                    "description": "text", 
                                    "speakers": "text", 
                                    "parent_session": "integer FOREIGN KEY (parent_session) REFERENCES sessions(sessionid)"})
    speaker_to_session =    db_table("speaker_to_session", 
                                    {"id": "integer PRIMARY KEY AUTOINCREMENT", 
                                    "speaker": "text", 
                                    "sessionid": "integer FOREIGN KEY (sessionid) REFERENCES sessions(sessionid)"})
    speaker_to_subsession = db_table("speaker_to_subsession", 
                                     {"id": "integer PRIMARY KEY AUTOINCREMENT", 
                                    "speaker": "text", 
                                    "sessionid": "integer FOREIGN KEY (subsessionid) REFERENCES subsessions(subsessionid)"})
    
    # TODO: process each entry from the data and add it to the right table

    sessions.close()
    subsessions.close()
    speaker_to_session.close()
    speaker_to_subsession.close()

def read_agenda(agenda_file):
    try:
        df = pd.read_excel(agenda_file, skiprows=14, engine='xlrd')
        print(df.columns.values)
        return df
    except Exception as e:
        print(f"Exception while reading the Excel file: {e}")

def main():
    parser = argparse.ArgumentParser(description='Agenda Importer')
    parser.add_argument('agenda', type=str, help='Agenda file to load')
    args = parser.parse_args()

    if not os.path.isfile(args.agenda):
        print(f"Error: '{args.agenda}' is not a valid file")
        return
    
    df = read_agenda(args.agenda)
    load_tables(df)

if __name__ == '__main__':
    main()