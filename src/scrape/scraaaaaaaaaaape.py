import requests
from bs4 import BeautifulSoup
import json
from time import sleep
import sys


def getData(url, headers):
    r = requests.get(url, headers=headers)
    return r.text


def validate(soup):
    # Validates page for correct format
    # Incorrect format example: https://www.themoviedb.org/movie/10
    dynamicLink = soup.find_all("link", rel="canonical")
    if 'collection' in dynamicLink[0]["href"]:
        return False

    # Validates page for content
    # No content example: https://www.themoviedb.org/movie/7
    error = soup.find_all("div", {"class": "error"})
    if len(error) != 0:
        return False

    return True


def scrape(url, database):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/116.0.0.0 Safari/537.36'
    }
    htmlRaw = getData(url=url, headers=headers)

    soup = BeautifulSoup(htmlRaw, 'html.parser')

    if validate(soup):
        movie = {}

        general_info = soup.find_all("div", {"class": "title"})[0]
        title = general_info.find("a").string.strip()
        if title not in database.keys():
            movie[title] = {}

            release_date = general_info.find("span", {"class": "release"}).string.strip()
            movie[title]["release_date"] = release_date

            genres = general_info.find("span", {"class": "genres"}).find_all("a")
            movie[title]["genres"] = []
            for genre in genres:
                movie[title]["genres"].append(genre.string.strip())

            runtime = general_info.find("span", {"class": "runtime"}).string.strip()
            movie[title]["runtime"] = runtime

            # Currently unused, holds information regarding movie summary and primary directors/producers
            header_info = soup.find("div", {"class": "header_info"})

            # Move to the appropriate page to obtain cast and crew info
            htmlCastRaw = getData(url=url + "/cast", headers=headers)
            castSoup = BeautifulSoup(htmlCastRaw, 'html.parser')

            panels = castSoup.find_all("section", {"class": "panel pad"})
            movie[title]["people"] = {"cast": {}, "crew": {}}

            cast_info = panels[0].ol
            if cast_info is not None:
                cast_list = cast_info.find_all("li")
                for cast in cast_list:
                    person = cast.p.find("a").string.strip()
                    character = cast.p.find("p", {"class": "character"}).string.strip()
                    movie[title]["people"]["cast"][person] = character
            crew_info = panels[1]
            if crew_info is not None:
                crew_wrappers = crew_info.find_all("div", {"class": "crew_wrapper"})
                for crew_sect in crew_wrappers:
                    sect = crew_sect.h4.string.strip()
                    movie[title]["people"]["crew"][sect] = {}

                    crew_list = crew_sect.ol.find_all("li")
                    for crew in crew_list:
                        person = crew.p.find("a").string.strip()
                        role = crew.find("p", {"class": "episode_count_crew"}).string.strip()
                        movie[title]["people"]["crew"][sect][person] = role

            print(movie)
            database[title] = movie[title]


def main(start, stop):
    BASE_URL = "https://www.themoviedb.org/movie/"
    with open("disgustingDatabase.json", 'r') as jFile:
        dataDict = json.load(jFile)

    for i in range(start, stop):
        print(i)
        scrape(BASE_URL + str(i), dataDict)
        # Delay so I don't get IP banned
        sleep(2.0)

    with open("disgustingDatabase.json", 'w') as jFile:
        json.dump(dataDict, jFile)


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) == 3:
        starting_index = int(sys.argv[1])
        ending_index = int(sys.argv[2])
        if starting_index >= ending_index:
            print("Invalid index range")
        else:
            main(starting_index, ending_index)
    else:
        print("Invalid number of arguments")
