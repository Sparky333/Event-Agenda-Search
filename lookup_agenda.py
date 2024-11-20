#!/usr/bin/env python3
import argparse
from db_table import db_table
import schemas
import os
from tabulate import tabulate
import textwrap
import subprocess

def wrap_text(info, width=50):
    """
    Wraps the text in all string fields of the dictionary to the given width.
    Args:
    - info (dict): The dictionary containing the data.
    - width (int): The max width for the wrapped text.
    
    Returns:
    - The dictionary with wrapped text in all string fields.
    """
    for field, value in info.items():
        if isinstance(value, str):  # Check if the value is a string
            wrapped_text = textwrap.fill(value, width)  # Wrap text at the specified width
            info[field] = wrapped_text
    return info

def filter_sess_info(info):
    """
    removes sessionid and subsessionid keys before printing
    """
    info = wrap_text(info)
    filtered_dict = {k: v for k, v in info.items() if k not in ["sessionid", "subsessionid"]}
    return filtered_dict
    #print(tabulate([filtered_dict], headers="keys", tablefmt="grid"))

def find_subsess_of_sess(sessionid):
    subsessions = db_table("subsessions", schemas.SUBSESSIONS_SCHEMA)

    subsess_of_sess = subsessions.select(["subsessionid","date", "time_start", "time_end", "type", "title", "location", "description", "speakers"], {"parent_session":sessionid})
    matchedSubsessionIDs = [subsess["subsessionid"] for subsess in subsess_of_sess]

    output = []

    for subsess in subsess_of_sess:
        output.append(filter_sess_info(subsess))

    return (output, matchedSubsessionIDs)

def lookup_speaker(value):
    sessions              = db_table("sessions", schemas.SESSIONS_SCHEMA)
    subsessions           = db_table("subsessions", schemas.SUBSESSIONS_SCHEMA)
    speaker_to_session    = db_table("speaker_to_session", schemas.SPEAKER_TO_SESSION_SCHEMA)
    speaker_to_subsession = db_table("speaker_to_subsession", schemas.SPEAKER_TO_SUBSESSION_SCHEMA)
    output = []

    matchedSubsessionIDs = []   # used to ensure no duplicate subsessions are outputted

    session_match = speaker_to_session.select(["sessionid"], {"speaker":value})
    for sess in session_match:
        sess_info = sessions.select(where={"sessionid":sess["sessionid"]})
        for s in sess_info:
            output.append(filter_sess_info(s))

        #matchedSubsessionIDs.extend(find_subsess_of_sess(sess["sessionid"]))
        subsess_output, matchedSubessIds = find_subsess_of_sess(sess["sessionid"])
        output.extend(subsess_output)
        matchedSubsessionIDs.extend(matchedSubessIds)

    matchedSubsessionIDs = set(matchedSubsessionIDs)

    subsession_match = speaker_to_subsession.select(["subsessionid"], {"speaker":value})
    for subsess in subsession_match:
        # if subsess was already added because its parent session was matched, skip
        if subsess["subsessionid"] in matchedSubsessionIDs:
            continue

        subsess_info = subsessions.select(where={"subsessionid":subsess["subsessionid"]})
        for ss in subsess_info:
            output.append(filter_sess_info(ss))

    table_str = tabulate(output, headers="keys", tablefmt="grid")
    subprocess.run(["less", "-S"], input=table_str.encode())

    sessions.close()
    subsessions.close()
    speaker_to_session.close()
    speaker_to_subsession.close()

def lookup(column, value):
    sessions              = db_table("sessions", schemas.SESSIONS_SCHEMA)
    subsessions           = db_table("subsessions", schemas.SUBSESSIONS_SCHEMA)
    output = []

    # search for sessions that match
    session_match = sessions.select(where = {column: value})

    matchedSubsessionIDs = []   # used to ensure no duplicate subsessions are outputted
    # for each matched session, search for subsesions of that session
    for sess in session_match:
        output.append(filter_sess_info(sess))
        subsess_output, matchedSubessIds = find_subsess_of_sess(sess["sessionid"])
        output.extend(subsess_output)
        matchedSubsessionIDs.extend(matchedSubessIds)

    matchedSubsessionIDs = set(matchedSubsessionIDs)

    # search for subsessions that match (their parent session didn't match)
    subsession_match = subsessions.select(["subsessionid","date", "time_start", "time_end", "type", "title", "location", "description", "speakers"], {column: value})
    for subsess in subsession_match:
        # if subsess was already added because its parent session was matched, skip
        if subsess["subsessionid"] in matchedSubsessionIDs: 
            continue

        output.append(filter_sess_info(subsess))

    table_str = tabulate(output, headers="keys", tablefmt="grid")
    subprocess.run(["less", "-S"], input=table_str.encode())

    sessions.close()
    subsessions.close()

def main():
    if not os.path.isfile("interview_test.db"):
        print("Error: please create database first by running import_agenda.py")
        return

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