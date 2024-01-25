#!/usr/bin/env python3

import os
import csv
import argparse
import sqlite3
import feedparser

import search

con = sqlite3.connect("tutorial.db")
cur = con.cursor()

archiveRss = os.path.join("rss","bestoftheworst_collection.rss")

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
    # Take all the movies and links we have, write it to a CSV
    # Also print to output
    res = cur.execute("SELECT * from movies")
    import code
    #code.interact(local=locals())
    print(res.fetchall())

def listMissing():
    res = cur.execute("SELECT title FROM movies WHERE  urls=''")
    movies = res.fetchall()
    return movies

def findMissing():
    movies = listMissing()
    for result in movies:
        title = result[0]
        url_list = search.findMovie(title)
        urlstring = ",".join(url_list)

        # TODO: Insert URLs into database
        cur.execute("UPDATE movies SET urls = ? WHERE title = ?", (urlstring, title))
        con.commit()

def parseRss():
    d = feedparser.parse(open(archiveRss).read())
    entries = d['entries']

    movies = listMissing()
    print("Missingmovies======")
    for movie in movies:
        movie = movie[0]
        print(movie)

        import code
        #code.interact(local=locals())

    print("Entries=====")
    for entry in entries:
        print(entry.title)
        if movie == entry.title:
            print(movie)
        #print("%s:%s" % (entry.title, entry.links[0]['href']))
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='HackFraud',
                    description='Finds free/ad supported movie watching links for BOTW movie database',
                    epilog='')
  
    parser.add_argument('-r', '--rebuild',
                    action='store_true',
                    help='Delete the database and rebuild from scratch')  # on/off flag

    parser.add_argument('-j', '--justwatch',
                    action='store_true',
                    help='Update movie DB by searching JustWatch for streaming links')  # on/off flag

    parser.add_argument('-a', '--archive',
                    action='store_true',
                    help='Update movie DB by searching Archive.org BOTW category')

    parser.add_argument('-d', '--dump',
                    action='store_true',
                    help='Print the contents of the DB')

    parser.add_argument('-l','--listmissing',
                    action='store_true',
                    help='Return a list of missing movies we still need links for')

    args = parser.parse_args()

    if args.justwatch:
        findMissing()

    elif args.archive:
        parseRss()

    elif args.listmissing:
        movies = listMissing()
        for movie in movies:
            # It's a list of tuples for some reason lmao
            print(movie[0])

    elif args.dump:
        dumpDb()
        
    # Only do this once if we need to
    #setupDb()
    #parseCsv()
    #dumpDb()
    
