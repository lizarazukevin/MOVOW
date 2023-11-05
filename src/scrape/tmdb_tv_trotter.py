import requests
from time import sleep
import re
import pymongo
import sys
import argparse


def main(start: int, stop: int, api_auth: str) -> None:
    BASE_URL = "https://api.themoviedb.org/3/tv/"
    try:
        client = pymongo.MongoClient("mongodb+srv://jasperemick:lB7P6QQdJtrox4k9"
                                     "@movow1.yk4hwgi.mongodb.net"
                                     "/?retryWrites=true&w=majority")
    except:
        return

    db = client.movow1

    headers = {
        "accept": "application/json",
        "Authorization": api_auth
    }

    show_collection = db["shows"]
    season_collection = show_collection["seasons"]
    episode_collection = season_collection["episodes"]
    people_collection = db["people"]
    review_collection = db["reviews"]
    providers_collection = db["providers"]

    show_collection.drop()
    show_collection.create_index("tag", unique=True)
    #
    season_collection.drop()
    season_collection.create_index("tag", unique=True)
    #
    episode_collection.drop()
    episode_collection.create_index("tag", unique=True)
    #
    people_collection.drop()
    people_collection.create_index("tag", unique=True)
    #
    review_collection.drop()
    # review_collection.create_index("tag", unique=True)
    #
    providers_collection.drop()

    for i in range(start, stop):
        print(i)
        tv_reaper(BASE_URL + str(i), show_collection, people_collection, review_collection, providers_collection,
                  headers)
        sleep(1.0)


def tv_reaper(url: str,
              show_collection: pymongo.collection.Collection,
              people_collection: pymongo.collection.Collection,
              review_collection: pymongo.collection.Collection,
              providers_collection: pymongo.collection.Collection,
              headers: dict) -> None:
    response = requests.get(url=url, headers=headers)
    details = response.json()
    # Cancels process if response is invalid
    if "success" in details.keys() and details["success"] is False:
        return
    """



        GET ALL OF THE IMPORTANT MOVIE DETAILS



    """
    tv_entry = {}
    # Provides movies with an incrementing ID that's protected by a unique tag
    movie_name = details["name"].replace(' ', '_').lower().strip()
    movie_name = re.sub(r'\W+', '', movie_name)
    date = details["first_air_date"].replace('-', '_').strip()
    id_tag_tv = movie_name + '_' + date
    # duplication prevention could be handled here
    if show_collection.find_one(filter={"tag": id_tag_tv}):
        print("Duplicate Show")
        return
    tv_index = len(list(show_collection.find()))

    # Get movie info
    tv_entry["id"] = tv_index
    tv_entry["tag"] = id_tag_tv
    tv_entry["title"] = details["name"]
    tv_entry["original_title"] = details["original_name"]
    tv_entry["initial_release_date"] = details["first_air_date"]
    tv_entry["final_release_date"] = details["last_air_date"]
    tv_entry["number_of_episodes"] = details["number_of_episodes"]
    tv_entry["number_of_seasons"] = details["number_of_seasons"]
    # The release status of the movie
    tv_entry["in_production"] = details["in_production"]
    tv_entry["status"] = details["status"]
    tv_entry["genres"] = []
    for genre in details["genres"]:
        tv_entry["genres"].append({
            "name": genre["name"]
        })
    # The audience's average rating for the film out of 10
    tv_entry["audience_rating"] = details["vote_average"]
    # The number of members who provided a rating for the film
    tv_entry["number_of_ratings"] = details["vote_count"]

    seasons_collection = show_collection["seasons"]

    tv_entry["seasons"] = []
    for season in details["seasons"]:

        season_entry = {}
        response_season = requests.get(url=url + "/season/" + str(season["season_number"]), headers=headers)

        details = response_season.json()
        print(details)
        season_name = details["name"].replace(' ', '_').lower().strip()
        season_name = re.sub(r'\W+', '', season_name)
        if details["air_date"]:
            date = details["air_date"].replace('-', '_').strip()
        else:
            date = "0000_00_00"
        id_tag_season = movie_name + '_' + season_name + '_' + date

        season_index = len(list(seasons_collection.find()))

        season_entry["id"] = season_index
        season_entry["tag"] = id_tag_season
        season_entry["name"] = details["name"]
        season_entry["order"] = details["season_number"]
        season_entry["show_id"] = tv_index
        season_entry["audience_rating"] = details["vote_average"]
        season_entry["number_of_ratings"] = None

        episode_collection = seasons_collection["episodes"]

        season_entry["episodes"] = []
        for episode in details["episodes"]:
            episode_entry = {}
            response_episode = requests.get(url=url + "/season/" + str(season["season_number"]) +
                                            "/episode/" + str(episode["episode_number"]), headers=headers)

            details = response_episode.json()
            print(details)

            episode_name = details["name"].replace(' ', '_').lower().strip()
            episode_name = re.sub(r'\W+', '', episode_name)
            if details["air_date"]:
                date = details["air_date"].replace('-', '_').strip()
            else:
                date = "0000_00_00"
            id_tag_episode = movie_name + '_' + season_name + '_' + episode_name + '_' + date

            episode_index = len(list(seasons_collection.find()))

            episode_entry["id"] = episode_index
            episode_entry["tag"] = id_tag_episode
            episode_entry["name"] = details["name"]
            episode_entry["order"] = details["episode_number"]
            episode_entry["season_id"] = season_index
            episode_entry["show_id"] = tv_index
            episode_entry["audience_rating"] = details["vote_average"]
            episode_entry["number_of_ratings"] = details["vote_count"]

            season_entry["episodes"].append({
                "id": episode_index,
                "name": episode_entry["name"],
                "order": episode_entry["order"]
            })
            response_episode.close()

            try:
                episode_collection.insert_one(episode_entry)
                print("Episode Added: ", episode_entry["name"])
            except:
                print("Failed to add Episode: ", episode_entry["name"])

        tv_entry["seasons"].append({
            "id": season_index,
            "name": season_entry["name"],
            "order": season_entry["order"]
        })
        response_season.close()

        try:
            seasons_collection.insert_one(season_entry)
            print("Season Added: ", season_entry["name"])
        except:
            print("Failed to add Season: ", season_entry["name"])

    response.close()

    """



        GET PEOPLE FROM THE MOVIE, REGISTER THEIR PROFILES AND ADD THEM TO THE MOVIE ENTRY



    """
    credits_url = url + "/credits"
    response = requests.get(url=credits_url, headers=headers)
    people = response.json()
    tv_entry["cast"] = []
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
        people_entry["cast_experience"] = [
            {
                "id": tv_index,
                "media_type": 1,
                "media": tv_entry["title"],
                "character": person["character"]
            }
        ]
        people_entry["crew_experience"] = []

        response_person.close()

        try:
            people_collection.insert_one(people_entry)
            print("Person Added: ", people_entry["name"])
        except pymongo.errors.DuplicateKeyError:
            people_collection.find_one_and_update(filter={"tag": id_tag_person},
                                                  update={"$push": {"cast_experience": {
                                                      "id": tv_index,
                                                      "media_type": 1,
                                                      "media": tv_entry["title"],
                                                      "character": person["character"]
                                                  }}})
            print("Duplicate Person: ", people_entry["name"])

        tv_entry["cast"].append({
            "id": person_index,
            "name": person["name"],
            "character": person["character"]
        })

    tv_entry["crew"] = []
    for person in people["crew"]:
        people_entry = {}

        response_person = requests.get(url="https://api.themoviedb.org/3/person/" + str(person["id"]), headers=headers)

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
        people_entry["cast_experience"] = []
        people_entry["crew_experience"] = [
            {
                "id": tv_index,
                "media_type": 1,
                "media": tv_entry["title"],
                "department": person["department"],
                "job": person["job"]
            }
        ]
        response_person.close()

        try:
            people_collection.insert_one(people_entry)
            print("Person Added: ", people_entry["name"])
        except pymongo.errors.DuplicateKeyError:
            # If the person already exists in the database only their experience is updated
            people_collection.find_one_and_update(filter={"tag": id_tag_person},
                                                  update={"$push": {"crew_experience": {
                                                      "id": tv_index,
                                                      "media_type": 1,
                                                      "media": tv_entry["title"],
                                                      "department": person["department"],
                                                      "job": person["job"]
                                                  }}})
            print("Duplicate Person: ", people_entry["name"])

        tv_entry["crew"].append({
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

    tv_entry["reviews"] = []
    for review in reviews_TMDB["results"]:
        review_entry = {}
        response_review = requests.get(url="https://api.themoviedb.org/3/review/" + str(review["id"]), headers=headers)

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
            print("Review Added: ", review_entry["author_username"])
        except pymongo.errors.DuplicateKeyError:
            print("Duplicate Review: ", review_entry["author_username"])

        tv_entry["reviews"].append({
            "id": review_index,
            "author_name": review["author_details"]["name"],
            "author_username": review["author_details"]["username"],
            "origin": "TMDB",
            "rating": review["author_details"]["rating"],
        })
    response.close()
    """



            PROVIDERS



        """
    providers_url = url + "/watch/providers"
    response = requests.get(url=providers_url, headers=headers)
    watch = response.json()

    tv_entry["providers"] = []
    for iso in watch["results"].keys():
        region = watch["results"][iso]
        print(region)

        renters = []
        if "rent" in region.keys():
            getProviders("rent", region, iso, renters, tv_entry, providers_collection)

        buyers = []
        if "buy" in region.keys():
            getProviders("buy", region, iso, buyers, tv_entry, providers_collection)

        flatrates = []
        if "flatrate" in region.keys():
            getProviders("flatrate", region, iso, flatrates, tv_entry, providers_collection)

        tv_entry["providers"].append({
            "region": str(iso),
            "rent": renters,
            "buy": buyers,
            "flatrate": flatrates
        })
    response.close()

    # Theoretically should never fail
    show_collection.insert_one(tv_entry)
    pass


def getProviders(method: str, region: dict, iso: any, provider_list: list, show_entry: dict,
                 providers_collection: pymongo.collection.Collection):
    for provider in region[method]:
        provider_list.append({
            "provider_name": provider["provider_name"]
        })
        provider_document = providers_collection.find_one({"name": provider["provider_name"]})
        if provider_document:

            if providers_collection.find_one(filter={"name": provider["provider_name"],
                                                     method + ".media": show_entry["title"]}):

                providers_collection.update_one(filter={"name": provider["provider_name"],
                                                        method + ".media": show_entry["title"]},
                                                update={"$push": {method + ".$.regions": iso}})
            else:
                providers_collection.update_one(filter={"name": provider["provider_name"]},
                                                update={"$push": {method: {
                                                    "id": show_entry["id"],
                                                    "media": show_entry["title"],
                                                    "regions": [iso]
                                                }}})
        else:
            provider_entry = {}
            provider_entry["id"] = len(list(providers_collection.find()))
            provider_entry["tag"] = None
            provider_entry["name"] = provider["provider_name"]
            provider_entry["rent"] = []
            provider_entry["buy"] = []
            provider_entry["flatrate"] = []
            provider_entry[method] = [{
                "id": show_entry["id"],
                "media": show_entry["title"],
                "regions": [iso]
            }]
            providers_collection.insert_one(provider_entry)

        print(list(providers_collection.find({"name": provider["provider_name"]})))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("movie trotter")
    parser.add_argument("start", help="The starting movie ID (int) value for the trotter to begin at")
    parser.add_argument("end", help="The final movie ID (int) value for the trotter to finish at")
    args = parser.parse_args()

    start = int(args.start)
    end = int(args.end)

    main(start, end, "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0NWFkMWQ5YzE0ZGVlNjAxZjJmMDZiNGZkY"
                     "jJmMmQ5NSIsInN1YiI6IjY1MWM1MzNlZWE4NGM3MDEwYzE0N2M5YiIsInNjb3BlcyI6WyJhcG"
                     "lfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.kaQbTtDsjaWixw5bn3RI-KpZJnHW622dbDbgThzrkaU")
