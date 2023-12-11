#!/usr/bin/env python3
import os

botw_main = os.path.join("csv","BoTW_Main.csv")
botw_spotlight = os.path.join("csv", "BoTW_Spotlight.csv")

def readCsvs():
    with open(botw_main, newline='') as maincsv:
        reader = csv.DictReader(maincsv)
        for row in reader:
            print(row['First Film'] + "\n" + row['Second Film'])
            import code
            code.interact(local=locals())

def writeCsv():
    # CSV Format should be:
    # Title, Type, URL1, URL2, URL3
    pass


if __name__ == "__main__":
    readCsvs()
