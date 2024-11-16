#!/usr/bin/env python3
import argparse
import os
import pandas as pd
from db_table import db_table
'''
TODO:
Add comments in code
Add Null or required attributes to table declarations
Adjust so names for columns aren't hardcoded are are instead dynamic based on excel column names
Check if we need to jump to the row "START YOUR AGENDA BELOW" or if data starts from row 1
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
                                    "parent_session": "integer",
                                    "FOREIGN KEY (parent_session)": "REFERENCES sessions(sessionid)"})
    speaker_to_session =    db_table("speaker_to_session", 
                                    {"id": "integer PRIMARY KEY AUTOINCREMENT", 
                                    "speaker": "text", 
                                    "sessionid": "integer",
                                    "FOREIGN KEY (sessionid)": "REFERENCES sessions(sessionid)"})
    speaker_to_subsession = db_table("speaker_to_subsession", 
                                     {"id": "integer PRIMARY KEY AUTOINCREMENT", 
                                    "speaker": "text", 
                                    "subsessionid": "integer",
                                    "FOREIGN KEY (subsessionid)": "REFERENCES subsessions(subsessionid)"})

    last_session_id = None  # latest inserted session each subsession refers to

    for _,row in df.iterrows():
        session_or_sub = row["*Session or \nSub-session(Sub)"]

        data = {
            "date": row["*Date"],
            "time_start": row["*Time Start"],
            "time_end": row["*Time End"],
            "session_title": row["*Session Title"],
            "location": row["Room/Location"],
            "description": row["Description"],
            "speakers": row["Speakers"]
        }

        # turn NaN vals to None
        data = {k: (None if pd.isna(v) else v) for k, v in data.items()}

        speakers = []
        # check if there are speakers for this event
        if not (pd.isna(data["speakers"]) or data["speakers"].strip() == ""):
            speakers = [speaker.strip() for speaker in row["Speakers"].split(";")]

        if session_or_sub == "Session":
            last_session_id = sessions.insert(data)
            for speaker in speakers:
                speaker_to_session.insert({"speaker": speaker, "sessionid": last_session_id})

        elif session_or_sub == "Sub":
            if last_session_id is None:
                print(f"Error: Missing parent session for subsession {data['session_title']}")
                continue
            
            data["parent_session"] = last_session_id
            subsessionid = subsessions.insert(data)
            for speaker in speakers:
                speaker_to_subsession.insert({"speaker": speaker, "subsessionid": subsessionid})

    sessions.close()
    subsessions.close()
    speaker_to_session.close()
    speaker_to_subsession.close()
    

def read_agenda(agenda_file):
    try:
        df = pd.read_excel(agenda_file, skiprows=14, engine='xlrd')
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

    print("SUCCESS! Finished running code")

if __name__ == '__main__':
    main()