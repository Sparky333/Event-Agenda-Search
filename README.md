### I. Import Agenda

This program imports the schedule of an event into a local SQLite database.

Run the program as follows:
`$> ./import_agenda.py agenda.xls`

- A sample agenda.xls file is provided. Please adhere to the same format.

### II. Lookup Agenda

This program finds agenda sessions in the data you imported.

Run the program as follows:
`$> ./lookup_agenda.py column value`

Where:

- column can be one of `["date", "time_start", "time_end", "title", "location", "description", "speaker"]`
- value is the expected value for that field

- The program will look for both sessions and subsessions
- For all matched session, it will return all its corresponding subsessions
- For speaker, it will return all sessions where we can find this speaker, even though they may not be the only speaker.

For example, given the data in the sample agenda.xls file:

$> ./lookup_agenda.py title Keynote:

will return:

```

+------------+--------------+------------+---------+-------------------------------------------+------------------------+----------------------------------------------------+-------------+
| date       | time_start   | time_end   | type    | title                                     | location               | description                                        | speakers    |
+============+==============+============+=========+===========================================+========================+====================================================+=============+
| 06/16/2018 | 08:45 AM     | 09:45 AM   | Session | Keynote:                                  |                        |                                                    |             |
+------------+--------------+------------+---------+-------------------------------------------+------------------------+----------------------------------------------------+-------------+
| 06/16/2018 | 08:45 AM     | 09:45 AM   | Sub     | Inside Windows Azure: The Challenges and  | South Pacific Ballroom | Cloud operating systems provide on-demand,         | Brad Calder |
|            |              |            |         | Opportunities of a Cloud Operating System |                        | scalable compute and storage resources. They allow |             |
|            |              |            |         |                                           |                        | service developers to focus on their business      |             |
|            |              |            |         |                                           |                        | logic by simplifying many portions of their        |             |
|            |              |            |         |                                           |                        | service, including resource management,            |             |
|            |              |            |         |                                           |                        | provisioning, monitoring, and application          |             |
|            |              |            |         |                                           |                        | lifecycle management. This talk describes some of  |             |
|            |              |            |         |                                           |                        | the technical challenges faced, as well as         |             |
|            |              |            |         |                                           |                        | emergent opportunities created, by Microsoft's     |             |
|            |              |            |         |                                           |                        | cloud operating system Windows Azure.              |             |
+------------+--------------+------------+---------+-------------------------------------------+------------------------+----------------------------------------------------+-------------+
```

The first row is returned as an exact match. The second row is returned since it is a subsession of the matched session.

### Requirements

Please note: Pandas needs to be installed to run the program
