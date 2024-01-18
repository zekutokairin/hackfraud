#!/usr/bin/env python3

import csv
import argparse
import sqlite3

import search

con = sqlite3.connect("tutorial.db")
cur = con.cursor()

def setupDb():
    # For now, urls will be a comma separated list of urls as a string
    cur.execute("CREATE TABLE movies(title type UNIQUE, type, urls)")

def parseCsv():
    # Intended to parse a CSV dumped from the Google Doc
    m = open("movies.csv", 'r')
    reader = csv.DictReader(m)
    for row in reader:
        try:
            cur.execute("INSERT INTO movies VALUES (?, ?, ?)", (row['Title'], row['Type'], ""))
            con.commit()
        except sqlite3.IntegrityError as e:
            print("Refusing to insert duplicate movie title: %s" % row['Title'])

def dumpDb():
    res = cur.execute("SELECT * from movies")
    print(res.fetchall())

def findMissing():
    res = cur.execute("SELECT title FROM movies WHERE  urls=''")
    movies = res.fetchall()

    for result in movies:
        title = result[0]
        url_list = search.findMovie(title)
        urlstring = ",".join(url_list)

        # TODO: Insert URLs into database
        cur.execute("UPDATE movies SET urls = ? WHERE title = ?", (urlstring, title))
        con.commit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='HackFraud',
                    description='Finds free/ad supported movie watching links for BOTW movie database',
                    epilog='')
  
    # TODO: add doc strings for this option
    parser.add_argument('-r', '--rebuild',
                    action='store_true')  # on/off flag

    parser.add_argument('-u', '--update',
                    action='store_true')  # on/off flag

    parser.add_argument('-p', '--print',
                    action='store_true')  # on/off flag



    args = parser.parse_args()

    if args.update:
        findMissing()

    elif args.print:
        dumpDb()
        
    # Only do this once if we need to
    #setupDb()
    #parseCsv()
    #dumpDb()
    
