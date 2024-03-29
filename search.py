#!/usr/bin/env py#thon3
import sys
import feedparser
from simplejustwatchapi.justwatch import search as jwsearch

COUNTRY = "US"
MONETIZATION_TYPES = ["FREE","ADS"]

# TODO: Parse the Archive.org collection RSS to get links
archive_rss = "https://archive.org/services/collection-rss.php?collection=bestoftheworst-collection"
# TODO: Figure out if there are any items in this search that are not also in the above collection
archive2_url = "https://archive.org/search?query=subject%3A%22Best%20of%20the%20Worst%22"
archive3_url = "https://archive.org/download/video_archive_553-cd-207"
# TODO: Somehow catalogue the titles of the Youtube playlist entries
instructional_url = "https://www.youtube.com/@instructionalvhstapeacrhiv2038/videos"
# Not sure if we want to use these, they may or may not be legit
ytp_url = "https://www.youtube.com/playlist?list=PL9XZF4i8A3ISHK7joPITYCATkIXjYFmfn"

def searchJustwatch(title):
    ret = []
    # Search JustWatch for multi-streaming services
    try:
        results = jwsearch(title, COUNTRY, "en", 5, True)
    except Exception as e:
        # The API wrapper may not cleanly parse all results, return empty list
        return []

    n = 0
    for movie in results:
        #print("============================")
        has_offer = False
        for offer in movie.offers:
            if offer.monetization_type in MONETIZATION_TYPES:
                #print("%s:%s" % (offer.name, offer.url))
                has_offer = True
        if has_offer:
            ret.append(movie)
        #print("============================")
    return ret

def dumpArchiveCollection():
    feed = feedparser.parse(archive_rss)
    movies = feed.get('entries')

    feed = feedparser.parse(archive2_url)



def searchArchiveCollection(title):
    # Search Archive.org RSS links
    feed = feedparser.parse(archive_rss)
    movies = feed.get('entries')
    for movie in movies:
        print(movie.get('title'))
        if title in movie.get('title'):
            print(movie.get('title') + "\t\t" + movie.get('links')[0]['href'])

def promptInt():
    ret = None
    while True:
        try:
            ret = int(input())
            return ret
        except ValueError:
            print("Please enter a valid number:")
        

def findMovie(title):
    print("*** Searching for movie: \"%s\"" % title)
    jw = searchJustwatch(title)
    n = 1

    urls = []

    
    if len(jw) > 0:
        for movie in jw:
            print("%d: %s (%d)" % (n, movie.title, movie.release_year))
            n+=1
        print("0: None of these")
        selection = promptInt()

        if selection > 0:
            selection-=1

            # Iterate through MONETIZATION_TYPES in order
            # This lets us prioritize Free movies over Ad supported.
            for mtype in MONETIZATION_TYPES:
                for offer in jw[selection].offers:
                    if offer.monetization_type == mtype:
                        urls.append(offer.url)
                        #print("%s:%s" % (offer.name, offer.url))

        # We're only going to return the first 3 URLs
    else:
        print("No matches found!\n")
    return urls[0:3]

    # TODO: if we don't have any matches, move to this step
    #searchArchiveCollection(title)
        
    # TODO: How can we programmatically use the archive.org subject search?
    # TODO Search Youtube instructional URL playlists
    return []

if __name__ == "__main__":
    # TODO: Option to write movie results to CSV
    findMovie(sys.argv[1])
