#!/usr/bin/env python3
from simplejustwatchapi.justwatch import search as jwsearch
import sys

COUNTRY = "US"
MONETIZATION_TYPES = ["FREE","ADS"]

archive_url = "https://archive.org/details/bestoftheworst-collection"
archive2_url = "https://archive.org/search?query=subject%3A%22Best%20of%20the%20Worst%22"
ytp_url = "https://www.youtube.com/playlist?list=PL9XZF4i8A3ISHK7joPITYCATkIXjYFmfn"
instructional_url = "https://www.youtube.com/@instructionalvhstapeacrhiv2038/videos"

# TODO: Get thumbnail if one does not exist

def findMovie(title):
    # Search JustWatch for multi-streaming services
    results = jwsearch(title, COUNTRY, "en", 5, True)
    #print(results)
    # TODO: Parse JW search results
    import code
    code.interact(local=locals())
    for movie in results:
        print("%s (%d)" % (movie.title, movie.release_year))
        print("============================")
        for offer in movie.offers:
            if offer.monetization_type in MONETIZATION_TYPES:
                print("%s:%s" % (offer.name, offer.url))
        print("============================")
        
    # Search Archive.org for weird instructional stuff
    # TODO: 

    # Search Youtube BOTW playlists

if __name__ == "__main__":
    findMovie(sys.argv[1])
