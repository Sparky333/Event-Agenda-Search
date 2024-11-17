#!/usr/bin/env python3
import argparse
from db_table import db_table
import schemas

'''
TODO:
Add unit tests:
title break should give len 7 results
title breakfast should give len 3 results

'''

def lookup_speaker(value):
    pass
def lookup(column, value):
    sessions =              db_table("sessions", schemas.SESSIONS_SCHEMA)
    subsessions =           db_table("subsessions", schemas.SUBSESSIONS_SCHEMA)
    speaker_to_session =    db_table("speaker_to_session", schemas.SPEAKER_TO_SESSION_SCHEMA)
    speaker_to_subsession = db_table("speaker_to_subsession", schemas.SPEAKER_TO_SUBSESSION_SCHEMA)

    print(len(sessions.select(["date", "time_start", "time_end", "type", "title", "location", "description", "speakers"], {column: value})))


def main():
    parser = argparse.ArgumentParser(description='Agenda Lookup')
    parser.add_argument('column', type=str, help='What column to match value on')
    parser.add_argument('value', type=str, help='What value to match')
    args = parser.parse_args()

    column = args.column.lower().strip()
    value = args.value.lower().strip()

    if column not in ["date", "time_start", "time_end", "title", "location", "description", "speaker"]:
        print(f"{args.column} is an invalid lookup column. Column must be one of " + \
              "date, time_start, time_end, title, location, description, speaker")
        return
    
    if column == "speaker":
        lookup_speaker(value)
    else:
        lookup(column, value)


if __name__ == "__main__":
    main()