#!/usr/bin/env python3
import sys
import feedparser
import csv
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
    for movie in results:
        print("%s (%d)" % (movie.title, movie.release_year))
        print("============================")
        for offer in movie.offers:
            if offer.monetization_type in MONETIZATION_TYPES:
                print("%s:%s" % (offer.name, offer.url))
        print("============================")

def searchArchiveCollection(title):
    # Search Archive.org RSS links
    feed = feedparser.parse(archive_rss)
    movies = feed.get('entries')
    for movie in movies:
        print(movie.get('title'))

def findMovie(title):
    searchJustwatch(title)
    searchArchiveCollection(title)
        
    # TODO: How can we programmatically use the archive.org subject search?

    # TODO Search Youtube instructional URL playlists

if __name__ == "__main__":
    findMovie(sys.argv[1])
