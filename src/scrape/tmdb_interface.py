import requests
from bs4 import BeautifulSoup
import json
from time import sleep
import sys

# TODO: Check for invalid movie ids before scraping API
# TODO: Add preventative measure for duplications

def main(start, stop):
    BASE_URL = "https://api.themoviedb.org/3/movie/"
    with open("data2.json", 'r') as jFile:
        dataDict = json.load(jFile)

    # for i in range(start, stop):
    #     print(i)
    consume(BASE_URL + str(11), dataDict)
        # Delay so I don't get IP banned
        #sleep(2.0)

    with open("data2.json", 'w') as jFile:
        json.dump(dataDict, jFile, indent=4)


def consume(url, database):
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0NWFkMWQ5YzE0ZGVlNjAxZjJmMDZiNGZkYjJmMmQ5NSIsInN1YiI6I"
                         "jY1MWM1MzNlZWE4NGM3MDEwYzE0N2M5YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.kaQbTtDsjaW"
                         "ixw5bn3RI-KpZJnHW622dbDbgThzrkaU"
    }
    entry = {}
    response = requests.get(url=url, headers=headers)
    details = response.json()
    entry["title"] = details["title"]
    entry["release_date"] = details["release_date"]
    entry["runtime"] = details["runtime"]
    # The release status of the movie
    entry["status"] = details["status"]
    entry["genres"] = []
    for genre in details["genres"]:
        entry["genres"].append({
            "name": genre["name"]
        })
    # The audience's average rating for the film out of 10
    entry["audience_rating"] = details["vote_average"]
    # The number of members who provided a rating for the film
    entry["number_of_ratings"] = details["vote_count"]
    response.close()

    credits_url = url + "/credits"
    response = requests.get(url=credits_url, headers=headers)
    people = response.json()
    entry["cast"] = []
    for person in people["cast"]:
        entry["cast"].append({
            "name": person["name"],
            "gender": person["gender"],
            "specialty": person["known_for_department"],
            "character": person["character"]
        })
    entry["crew"] = []
    for person in people["crew"]:
        entry["crew"].append({
            "name": person["name"],
            "gender": person["gender"],
            "specialty": person["known_for_department"],
            "department": person["department"],
            "job": person["job"]
        })
    response.close()

    reviews_url = url + "/reviews"
    response = requests.get(url=reviews_url, headers=headers)
    reviews_TMDB = response.json()

    entry["reviews"] = []
    for review in reviews_TMDB["results"]:

        author_details = [{
            "name": review["author_details"]["name"],
            "username_tmdb": review["author_details"]["username"],
            "rating": review["author_details"]["rating"]
        }]

        entry["reviews"].append({
            "author_details": author_details,
            "content": review["content"],
            "date_created": review["created_at"],
            "date_updated": review["updated_at"],
            "url_tmdb": review["url"]
        })
    response.close()

    providers_url = url + "/watch/providers"
    response = requests.get(url=providers_url, headers=headers)
    watch = response.json()

    entry["providers"] = []

    for key in watch["results"].keys():
        language = watch["results"][key]

        renters = []
        if "rent" in language.keys():
            for renter in language["rent"]:
                renters.append({
                    "provider_name": renter["provider_name"]
                })
        buyers = []
        if "buy" in language.keys():
            for buyer in language["buy"]:
                buyers.append({
                    "provider_name": buyer["provider_name"]
                })
        flatrates = []
        if "flatrate" in language.keys():
            for flats in language["flatrate"]:
                flatrates.append({
                    "provider_name": flats["provider_name"]
                })

        entry["providers"].append({
            "country": str(key),
            "rent": renters,
            "buy": buyers,
            "flatrate": flatrates
        })
    response.close()
    database.append(entry)


if __name__ == "__main__":
    main(7, 100)
