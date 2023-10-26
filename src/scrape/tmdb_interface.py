import requests
from bs4 import BeautifulSoup
import json
from time import sleep
import sys
import re
import pymongo


def main(start: int, stop: int, media: str) -> None:
    BASE_URL = "https://api.themoviedb.org/3/" + media + "/"
    try:
        client = pymongo.MongoClient("mongodb+srv://jasperemick:lB7P6QQdJtrox4k9"
                                     "@movow1.yk4hwgi.mongodb.net"
                                     "/?retryWrites=true&w=majority")
    except:
        pass

    db = client.movow1

    # with open(media + "_data.json", 'r') as dFile:
    #     dataDict = json.load(dFile)
    # with open(media + "_id.json", 'r') as iFile:
    #     idDict = json.load(iFile)

    if media == "movie":
        reaper = movie_reaper
    else:
        reaper = tv_reaper

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0NWFkMWQ5YzE0ZGVlNjAxZjJmMDZiNGZkYjJmMmQ5NSIsInN1YiI6I"
                         "jY1MWM1MzNlZWE4NGM3MDEwYzE0N2M5YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.kaQbTtDsjaW"
                         "ixw5bn3RI-KpZJnHW622dbDbgThzrkaU"
    }

    movie_collection = db["movies"]
    people_collection = db["people"]
    review_collection = db["reviews"]

    movie_collection.drop()
    movie_collection.create_index("tag", unique=True)

    people_collection.drop()
    people_collection.create_index("tag", unique=True)

    review_collection.drop()
    review_collection.create_index("tag", unique=True)

    for i in range(start, stop):
        print(i)
        reaper(BASE_URL + str(i), movie_collection, people_collection, review_collection, headers)
        sleep(1.0)

    list(movie_collection.find())
    # res = people_collection.insert_many(personDict)

    # print(res)
    #
    # with open(media + "_data.json", 'w') as dFile:
    #     json.dump(dataDict, dFile, indent=4)
    # with open(media + "_id.json", 'w') as iFile:
    #     json.dump(idDict, iFile, indent=4)


def tv_reaper(url: str, database: list, peoplebase: list, identification: dict, headers: dict) -> None:
    response = requests.get(url=url + "/season/3", headers=headers)
    details = response.json()
    print(url)
    if "success" in details.keys() and details["success"] is False:
        return
    entry = {}
    # An effort to id movies/prevent duplicates, most likely flawed in some edge cases
    if details["name"] in identification["shows"].keys():
        return
    size = len(identification["shows"].keys())
    name = details["name"].replace(' ', '_').strip().lower()
    identification["shows"][name] = size
    entry["id"] = size

    database.append(details)


def movie_reaper(url: str,
                 movie_collection: pymongo.collection.Collection,
                 people_collection: pymongo.collection.Collection,
                 review_collection: pymongo.collection.Collection,
                 headers: dict) -> None:
    response = requests.get(url=url, headers=headers)
    details = response.json()
    print(url)
    # Cancels process if response is invalid
    if "success" in details.keys() and details["success"] is False:
        return
    """
    
    
    
        GET ALL OF THE IMPORTANT MOVIE DETAILS
        
        
        
    """
    movie_entry = {}
    # Provides movies with an incrementing ID that's protected by a unique tag
    name = details["title"].replace(' ', '_').lower().strip()
    name = re.sub(r'\W+', '', name)
    date = details["release_date"].replace('-', '_').strip()
    id_tag_movie = name + '_' + date

    movie_index = len(list(movie_collection.find()))

    # Get movie info
    movie_entry["id"] = movie_index
    movie_entry["tag"] = id_tag_movie
    movie_entry["title"] = details["title"]
    movie_entry["original_title"] = details["original_title"]
    movie_entry["release_date"] = details["release_date"]
    movie_entry["runtime"] = details["runtime"]
    # The release status of the movie
    movie_entry["status"] = details["status"]
    movie_entry["genres"] = []
    for genre in details["genres"]:
        movie_entry["genres"].append({
            "name": genre["name"]
        })
    # The audience's average rating for the film out of 10
    movie_entry["audience_rating"] = details["vote_average"]
    # The number of members who provided a rating for the film
    movie_entry["number_of_ratings"] = details["vote_count"]
    response.close()
    """
    
    
    
        GET PEOPLE FROM THE MOVIE, REGISTER THEIR PROFILES AND ADD THEM TO THE MOVIE ENTRY
        
        
        
    """
    credits_url = url + "/credits"
    response = requests.get(url=credits_url, headers=headers)
    people = response.json()
    movie_entry["cast"] = []
    for person in people["cast"]:
        people_entry = {}

        personUrl = "https://api.themoviedb.org/3/person/" + str(person["id"])
        response_person = requests.get(url=personUrl, headers=headers)

        details = response_person.json()

        name = details["name"].replace(' ', '_').lower().strip()
        try:
            birth = details["birthday"].replace('-', '_').strip()
        except AttributeError:
            birth = "0000_00_00"
        id_tag_person = name + '_' + birth

        person_index = len(list(people_collection.find()))

        people_entry["id"] = person_index
        people_entry["tag"] = id_tag_person
        people_entry["name"] = details["name"]
        people_entry["also_known_as"] = details["also_known_as"]
        people_entry["birthday"] = details["birthday"]
        people_entry["death"] = details["deathday"]
        people_entry["gender"] = details["gender"]
        people_entry["popular_department"] = details["known_for_department"]

        response_person.close()

        try:
            people_collection.insert_one(people_entry)
            print("Person Added: ", people_entry["name"])
        except pymongo.errors.DuplicateKeyError:
            print("Duplicate Person: ", people_entry["name"])

        movie_entry["cast"].append({
            "id": person_index,
            "name": person["name"],
            "character": person["character"]
        })

    movie_entry["crew"] = []
    for person in people["crew"]:
        people_entry = {}

        personUrl = "https://api.themoviedb.org/3/person/" + str(person["id"])
        response_person = requests.get(url=personUrl, headers=headers)

        details = response_person.json()

        name = details["name"].replace(' ', '_').lower().strip()
        try:
            birth = details["birthday"].replace('-', '_').strip()
        except AttributeError:
            birth = "0000_00_00"
        id_tag_person = name + '_' + birth

        person_index = len(list(people_collection.find()))

        people_entry["id"] = person_index
        people_entry["tag"] = id_tag_person
        people_entry["name"] = details["name"]
        people_entry["also_known_as"] = details["also_known_as"]
        people_entry["birthday"] = details["birthday"]
        people_entry["death"] = details["deathday"]
        people_entry["gender"] = details["gender"]
        people_entry["popular_department"] = details["known_for_department"]

        response_person.close()

        try:
            people_collection.insert_one(people_entry)
            print("Person Added: ", people_entry["name"])
        except pymongo.errors.DuplicateKeyError:
            print("Duplicate Person: ", people_entry["name"])

        movie_entry["crew"].append({
            "id": person_index,
            "name": person["name"],
            "department": person["department"],
            "job": person["job"]
        })
    response.close()
    """      
    
    
     
        REVIEWS
        
        
        
    """
    reviews_url = url + "/reviews"
    response = requests.get(url=reviews_url, headers=headers)
    reviews_TMDB = response.json()

    movie_entry["reviews"] = []
    for review in reviews_TMDB["results"]:
        review_entry = {}
        reviewsurl = "https://api.themoviedb.org/3/review/" + str(review["id"])
        response_review = requests.get(url=reviewsurl, headers=headers)

        details = response_review.json()
        name = details["author_details"]["username"].replace(' ', '_').lower().strip()
        name = re.sub(r'\W+', '', name)
        title = details["media_title"].replace('-', '_').lower().strip()
        title = re.sub(r'\W+', '', title)
        id_tag_review = name + '_' + title

        review_index = len(list(review_collection.find()))

        review_entry["id"] = review_index
        review_entry["tag"] = id_tag_review
        review_entry["author_name"] = details["author_details"]["name"]
        review_entry["author_username"] = details["author_details"]["username"]
        review_entry["rating"] = details["author_details"]["rating"]
        review_entry["origin"] = "TMDB"
        review_entry["content"] = details["content"]
        review_entry["media_id"] = details["media_id"]
        review_entry["media"] = details["media_title"]
        review_entry["media_type"] = details["media_type"]
        review_entry["created"] = details["created_at"]
        review_entry["updated"] = details["updated_at"]
        review_entry["reference"] = details["url"]

        response_review.close()

        try:
            review_collection.insert_one(review_entry)
            print("Review Added: ", review_entry["author_name"])
        except pymongo.errors.DuplicateKeyError:
            print("Duplicate Person: ", review_entry["author_name"])

        movie_entry["reviews"].append({
            "id": review_index,
            "author_name": review["author_details"]["name"],
            "author_username": review["author_details"]["username"],
            "origin": "TMDB",
            "rating": review["author_details"]["rating"],
        })
    response.close()
    try:
        movie_collection.insert_one(movie_entry)
        print("Movie Added: ", movie_entry["title"])
    except pymongo.errors.DuplicateKeyError:
        print("Duplicate Movie: ", movie_entry["title"])
    return
    """
    
    
    
        PROVIDERS - NOT IMPLEMENTED
    
    
    
    """
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
    main(0, 10, "movie")
