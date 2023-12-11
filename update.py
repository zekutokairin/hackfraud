#!/usr/bin/env python3
import os
import csv

import search

botw_main = os.path.join("csv","BoTW_Main.csv")
botw_spotlight = os.path.join("csv", "BoTW_Spotlight.csv")

def readCsvs():
    with open(botw_main, newline='') as maincsv:
        fieldnames = ['Title', 'Type','URL1','URL2','URL3']
        with open("output.csv", 'w', newline='') as outputcsv:
            reader = csv.DictReader(maincsv)
            writer = csv.DictWriter(outputcsv,fieldnames)
            writer.writeheader()
            for row in reader:
                if row['First Film']:
                    writer.writerow({'Title': row['First Film'], 'Type':row['Gimmick'],'URL1':None,'URL2':None,'URL3':None})

                if row['Second Film']:
                    writer.writerow({'Title': row['Second Film'], 'Type':row['Gimmick'],'URL1':None,'URL2':None,'URL3':None})

                if row['Third Film']:
                    writer.writerow({'Title': row['Third Film'], 'Type':row['Gimmick'],'URL1':None,'URL2':None,'URL3':None})

                if row['Non-Reviewed / Extra Videos']:
                    writer.writerow({'Title': row['Non-Reviewed / Extra Videos'], 'Type':row['Gimmick'],'URL1':None,'URL2':None,'URL3':None})

def listMissing():
    # Parse through our current BOTW Link catalog and find movies with
    #   no streaming links.
    with open("output.csv", newline='') as outputcsv:
        reader = csv.DictReader(outputcsv)
        for row in reader:
            if not row['URL1'] and not row['URL2'] and not row['URL3']:
                print("Missing Video Links for: %s" % row['Title'])

def writeCsv():
    # CSV Format should be:
    # Title, Type, URL1, URL2, URL3
    pass

if __name__ == "__main__":
    # Warning! You only ever need to do readCsvs when you want to
    #   overwrite the entire list! You will lose all the URLs!
    #readCsvs()
    listMissing()
