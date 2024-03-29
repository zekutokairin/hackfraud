#!/usr/bin/env python3
import os
import csv
import json

import search

import argparse


botw_main = os.path.join("csv","BoTW_Main.csv")
botw_spotlight = os.path.join("csv", "BoTW_Spotlight.csv")
sheets = [botw_main, botw_spotlight]

def parseSpotlightCsv():
    # Return a list of Spotlight movie titles
    ret = []
    with open(botw_spotlight, newline='') as maincsv:
        fieldnames = ['Title', 'Type','URL1','URL2','URL3']
        with open("output.csv", 'a', newline='') as outputcsv:
            reader = csv.DictReader(maincsv)
            writer = csv.DictWriter(outputcsv,fieldnames)
            writer.writeheader()
            for row in reader:
                ret.append(row['Film'])
                writer.writerow({'Title': row['Film'], 'Type':'Spotlight'})
    return ret

def parseMainCsv(writecsv=False):
    # Returns a list of movie titles in the CSV
    # If writecsv=True, write an output file too
    ret = []
    with open(botw_main, newline='') as maincsv:
        fieldnames = ['Title', 'Type','URL1','URL2','URL3']
        with open("output.csv", 'a', newline='') as outputcsv:
            reader = csv.DictReader(maincsv)
            writer = csv.DictWriter(outputcsv,fieldnames)
            writer.writeheader()
            for row in reader:
                if row['First Film']:
                    ret.append(row['First Film'])
                    writer.writerow({'Title': row['First Film'], 'Type':row['Gimmick'],'URL1':None,'URL2':None,'URL3':None})

                if row['Second Film']:
                    ret.append(row['Second Film'])
                    writer.writerow({'Title': row['Second Film'], 'Type':row['Gimmick'],'URL1':None,'URL2':None,'URL3':None})

                if row['Third Film']:
                    ret.append(row['Third Film'])
                    writer.writerow({'Title': row['Third Film'], 'Type':row['Gimmick'],'URL1':None,'URL2':None,'URL3':None})

                if row['Non-Reviewed / Extra Videos']:
                    ret.append(row['Non-Reviewed / Extra Videos'])
                    writer.writerow({'Title': row['Non-Reviewed / Extra Videos'], 'Type':row['Gimmick'],'URL1':None,'URL2':None,'URL3':None})
    return ret

def listMissing(movie_dict):
    # Parse through our current BOTW Link catalog and find movies with
    #   no streaming links.
    nourl_titles = []

    for title, url_list in movie_dict.items():
        url1, url2, url3 = url_list
        if not url1 and not url2 and not url3:
            print("Missing Video Links for: %s" % title)
            nourl_titles.append(title)

    return nourl_titles
            

def update():
    # 1) Parse through the Movie DB and find movies with no links
    # 2) Search API for movie offerings
    # 3) Prompt user for match and populate offerings in DB
    master_dict = {}
    with open("movies.csv", 'r', newline='') as mastercsv:
        reader = csv.DictReader(mastercsv)
        for row in reader:
            key = row['Title']
            master_dict[key] = [row['URL1'],row['URL2'],row['URL3']]

    missing = listMissing(master_dict)

    for title in missing:
        search.findMovie(title)
    # Get back a list of URLs
    # TODO: Update the master_dict with those URLs
    # TODO: Write master_dict to new CSV

def writeToCsv():
    # CSV Format should be:
    # Title, Type, URL1, URL2, URL3
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='HackFraud',
                    description='Finds free/ad supported movie watching links for BOTW movie database',
                    epilog='')

    parser.add_argument('-r', '--rebuild',
                    action='store_true')  # on/off flag


    parser.add_argument('-u', '--update',
                    action='store_true')  # on/off flag

    args = parser.parse_args()

    # TODO: 
    if args.rebuild:
        print("Are you SURE you want to do this? It will remove all existing movie URLs and attempt to re-fetch all of them! [y/N]")
        prompt = input()
        if prompt.lower() == "y":
            print("Rebuilding...")

            # Parse the latest CSV files from Google Doc into movie title list 
            main = parseMainCsv()
            spotlight = parseSpotlightCsv()

            all_movies = main + spotlight

    elif args.update:
        update()
