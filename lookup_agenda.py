#!/usr/bin/env python3
import argparse
from db_table import db_table
import schemas

'''
TODO:
remove id from output since not wanted in output
'''

def lookup_speaker(value):
    sessions              = db_table("sessions", schemas.SESSIONS_SCHEMA)
    subsessions           = db_table("subsessions", schemas.SUBSESSIONS_SCHEMA)
    speaker_to_session    = db_table("speaker_to_session", schemas.SPEAKER_TO_SESSION_SCHEMA)
    speaker_to_subsession = db_table("speaker_to_subsession", schemas.SPEAKER_TO_SUBSESSION_SCHEMA)
    output                = ""

    matchedSubsessionIDs = []   # used to ensure no duplicate subsessions are outputted

    session_match = speaker_to_session.select(["sessionid"], {"speaker":value})
    for sess in session_match:
        sess_info = sessions.select(where={"sessionid":sess["sessionid"]})
        for s in sess_info:
            output += str(s) + "\n"

        subsess_of_sess = subsessions.select(["subsessionid","date", "time_start", "time_end", "type", "title", "location", "description", "speakers"], {"parent_session":sess["sessionid"]})
        matchedSubsessionIDs = [subsess["subsessionid"] for subsess in subsess_of_sess]

        for subsess in subsess_of_sess:
            output += str(subsess) + "\n"

    subsession_match = speaker_to_subsession.select(["subsessionid"], {"speaker":value})
    for subsess in subsession_match:
        if subsess["subsessionid"] in matchedSubsessionIDs:
            continue
        subsess_info = subsessions.select(where={"subsessionid":subsess["subsessionid"]})
        for ss in subsess_info:
            output += str(ss) + "\n"

    print(output)

    sessions.close()
    subsessions.close()
    speaker_to_session.close()
    speaker_to_subsession.close()


def lookup(column, value):
    sessions              = db_table("sessions", schemas.SESSIONS_SCHEMA)
    subsessions           = db_table("subsessions", schemas.SUBSESSIONS_SCHEMA)
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

    sessions.close()
    subsessions.close()

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