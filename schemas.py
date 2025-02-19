SESSIONS_SCHEMA              = {"sessionid": "integer PRIMARY KEY AUTOINCREMENT", 
                                "date": "text NOT NULL", 
                                "time_start": "text NOT NULL", 
                                "time_end": "text NOT NULL", 
                                "type": "text NOT NULL",
                                "title": "text NOT NULL", 
                                "location": "text", 
                                "description": "text", 
                                "speakers": "text"}

SUBSESSIONS_SCHEMA           = {"subsessionid": "integer PRIMARY KEY AUTOINCREMENT", 
                                "date": "text NOT NULL", 
                                "time_start": "text NOT NULL", 
                                "time_end": "text NOT NULL", 
                                "type": "text NOT NULL",
                                "title": "text NOT NULL",  
                                "location": "text", 
                                "description": "text", 
                                "speakers": "text",
                                "parent_session": "integer NOT NULL",
                                "FOREIGN KEY (parent_session)": "REFERENCES sessions(sessionid)"}

SPEAKER_TO_SESSION_SCHEMA    = {"id": "integer PRIMARY KEY AUTOINCREMENT", 
                                "speaker": "text NOT NULL", 
                                "sessionid": "integer NOT NULL",
                                "FOREIGN KEY (sessionid)": "REFERENCES sessions(sessionid)"}

SPEAKER_TO_SUBSESSION_SCHEMA = {"id": "integer PRIMARY KEY AUTOINCREMENT", 
                                "speaker": "text NOT NULL", 
                                "subsessionid": "integer NOT NULL",
                                "FOREIGN KEY (subsessionid)": "REFERENCES subsessions(subsessionid)"}