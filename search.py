#!/usr/bin/env python3
import sys
import feedparser
from simplejustwatchapi.justwatch import search as jwsearch

COUNTRY = "US"
MONETIZATION_TYPES = ["FREE","ADS"]

archive_rss = "https://archive.org/services/collection-rss.php?collection=bestoftheworst-collection"
archive2_url = "https://archive.org/search?query=subject%3A%22Best%20of%20the%20Worst%22"
instructional_url = "https://www.youtube.com/@instructionalvhstapeacrhiv2038/videos"
# Not sure if we want to use these, they may or may not be legit
ytp_url = "https://www.youtube.com/playlist?list=PL9XZF4i8A3ISHK7joPITYCATkIXjYFmfn"

def searchJustwatch(title):
    # Search JustWatch for multi-streaming services
    results = jwsearch(title, COUNTRY, "en", 5, True)
    ret = []
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

def searchArchiveCollection(title):
    # Search Archive.org RSS links
    feed = feedparser.parse(archive_rss)
    movies = feed.get('entries')
    for movie in movies:
        print(movie.get('title'))
        if title in movie.get('title'):
            print(movie.get('title') + "\t\t" + movie.get('links')[0]['href'])

def findMovie(title):
    jw = searchJustwatch(title)
    n = 1
    movies = []
    for movie in jw:
        print("%d: %s (%d)" % (n, movie.title, movie.release_year))
        n+=1
    print("0: None of these")
    # TODO: Prompt user to select movie
    selection = int(input())
    selection-=1
    for offer in jw[selection].offers:
        if offer.monetization_type in MONETIZATION_TYPES:
            print("%s:%s" % (offer.name, offer.url))


    #searchArchiveCollection(title)
        
    # TODO: How can we programmatically use the archive.org subject search?
    # TODO Search Youtube instructional URL playlists

if __name__ == "__main__":
    # TODO: Option to write movie results to CSV
    findMovie(sys.argv[1])
