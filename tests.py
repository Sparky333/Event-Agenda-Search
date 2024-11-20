#!/usr/bin/env python3
from db_table import db_table
import schemas
import subprocess
import os

def run_tests():
    sessions              = db_table("sessions", schemas.SESSIONS_SCHEMA)
    subsessions           = db_table("subsessions", schemas.SUBSESSIONS_SCHEMA)
    speaker_to_session    = db_table("speaker_to_session", schemas.SPEAKER_TO_SESSION_SCHEMA)
    speaker_to_subsession = db_table("speaker_to_subsession", schemas.SPEAKER_TO_SUBSESSION_SCHEMA)

    # some tests for import_agenda.py
    assert(len(sessions.select(where={"title":"Breakfast"})) == 3)
    assert(len(sessions.select(where={"title":"Break"})) == 7)
    assert(len(sessions.select(where={"location":"CoRaL loungE"})) == 7)
    assert(len(sessions.select(where={"location":"lobby"})) == 3)
    assert(len(speaker_to_session.select(where={"speaker":"john regehr"})) == 2)
    assert(len(speaker_to_subsession.select(where={"speaker":"yehuda afek"})) == 1)
    assert(len(sessions.select(where={"description":"<p>&nbsp;This is the Breakfast session!</p>"})) == 1)
    
    sessions.close()
    subsessions.close()
    speaker_to_session.close()
    speaker_to_subsession.close()


def main():
    if not os.path.isfile("interview_test.db"):
        result = subprocess.run(['./import_agenda.py', 'agenda.xls'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")

    run_tests()
    print("All tests passed!")

if __name__ == "__main__":
    main()