#!/usr/bin/env python3
import argparse
from db_table import db_table
import schemas

'''
TODO:
Turn everything to lowercase when checking for match? 
'''

def lookup_speaker(value):
    pass
def lookup(column, value):
    sessions =              db_table("sessions", schemas.SESSIONS_SCHEMA)
    subsessions =           db_table("subsessions", schemas.SUBSESSIONS_SCHEMA)
    speaker_to_session =    db_table("speaker_to_session", schemas.SPEAKER_TO_SESSION_SCHEMA)
    speaker_to_subsession = db_table("speaker_to_subsession", schemas.SPEAKER_TO_SUBSESSION_SCHEMA)


def main():
    parser = argparse.ArgumentParser(description='Agenda Lookup')
    parser.add_argument('column', type=str, help='What column to match value on')
    parser.add_argument('value', type=str, help='What value to match')
    args = parser.parse_args()

    column = args.column.lower()

    if column not in ["date", "time_start", "time_end", "title", "location", "description", "speaker"]:
        print(f"{args.column} is an invalid lookup column. Column must be one of " + \
              "date, time_start, time_end, title, location, description, speaker")
        return
    
    if column == "speaker":
        lookup_speaker(args.value)
    else:
        lookup(column, args.value)


if __name__ == "__main__":
    main()