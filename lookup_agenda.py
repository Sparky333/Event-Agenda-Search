#!/usr/bin/env python3
import argparse
from db_table import db_table
import schemas

'''
TODO:
Add unit tests:
title break should give len 7 results
title breakfast should give len 3 results
location "coral loune" should give 7
location "lobby" should give 3 results

search for debate should give one subsession
'''

def lookup_speaker(value):
    pass
def lookup(column, value):
    sessions              = db_table("sessions", schemas.SESSIONS_SCHEMA)
    subsessions           = db_table("subsessions", schemas.SUBSESSIONS_SCHEMA)
    speaker_to_session    = db_table("speaker_to_session", schemas.SPEAKER_TO_SESSION_SCHEMA)
    speaker_to_subsession = db_table("speaker_to_subsession", schemas.SPEAKER_TO_SUBSESSION_SCHEMA)
    output                = ""

    # search for sessions that match
    session_match = sessions.select(where = {column: value})

    matchedSubsessionIDs = []   # used to ensure no duplicate subsessions are outputted
    # for each matched session, search for subsesions of that session
    for sess in session_match:
        output += str(sess) + "\n"

        subsess_of_sess = subsessions.select(["subsessionid","date", "time_start", "time_end", "type", "title", "location", "description", "speakers"], {"parent_session":sess["sessionid"]})
        matchedSubsessionIDs = [subsess["subsessionid"] for subsess in subsess_of_sess]

        for subsess in subsess_of_sess:
            output += str(subsess) + "\n"

    matchedSubsessionIDs = set(matchedSubsessionIDs)

    # search for subsessions that match (their parent session didn't match)
    subsession_match = subsessions.select(["subsessionid","date", "time_start", "time_end", "type", "title", "location", "description", "speakers"], {column: value})
    for subsess in subsession_match:
        # if subsess was already added because its parent session was matched, skip
        if subsess["subsessionid"] in matchedSubsessionIDs: 
            continue

        for s in subsess:
            output += str(s) + "\n"

    print(output)

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