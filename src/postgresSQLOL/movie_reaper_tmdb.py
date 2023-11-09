from time import sleep
import argparse
import sys
import psycopg2


def main(start: int, stop: int, api_auth: str) -> None:
    BASE_URL = "https://api.themoviedb.org/3/movie/"

    headers = {
        "accept": "application/json",
        "Authorization": api_auth
    }

    conn = psycopg2.connect(
        host="localhost",
        database="movow1",
        user="postgres",
        password="OrangePotato#546-213")

    cur = conn.cursor()

    cur.execute()

    # for i in range(start, stop):
    #     print(i)
    #     movie_reaper(BASE_URL + str(i), movie_collection, people_collection, review_collection, providers_collection,
    #                  headers)
    #     sleep(1.0)


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
