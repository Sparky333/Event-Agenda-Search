#!/usr/bin/env python3
import argparse
import os
import pandas as pd

def read_agenda(agenda_file):
    try:
        df = pd.read_excel(agenda_file, skiprows=14, engine='xlrd')
        print(df.head())
    except Exception as e:
        print(f"Exception while reading the Excel file: {e}")

def main():
    parser = argparse.ArgumentParser(description='Agenda Importer')
    parser.add_argument('agenda', type=str, required=True,
                      help='Agenda file to load into the database')
    
    args = parser.parse_args()

    if not os.path.isfile(args.agenda):
        print(f"Error: '{args.agenda}' is not a valid file")
        return

if __name__ == '__main__':
    main()