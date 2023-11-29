from time import sleep
import argparse
import sys
import psycopg2
from config import config
import requests
import re
from psycopg2 import sql
from credit_reaper import credit_reaper


def main(start: int, stop: int, api_auth: str) -> None:
    BASE_URL = "https://api.themoviedb.org/3/movie/"

    headers = {
        "accept": "application/json",
        "Authorization": api_auth
    }

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        # create table one by one
        for i in range(start, stop):
            print(i)
            movie_reaper(BASE_URL + str(i), cur, conn, headers)
            sleep(1.0)
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def movie_reaper(url: str, cursor: any, conn: any, headers: dict) -> None:
    response = requests.get(url=url, headers=headers)
    details = response.json()
    print(url)
    # Cancels process if response is invalid
    if "success" in details.keys() and details["success"] is False:
        return
    """
    --------------------------------------------------------------------------------------------------------------------
        GET ALL OF THE IMPORTANT MOVIE DETAILS
    --------------------------------------------------------------------------------------------------------------------
    """
    # Provides movies with an incrementing ID that's protected by a unique tag
    name = details["title"].replace(' ', '_').lower().strip()
    name = re.sub(r'\W+', '', name)
    date = details["release_date"].replace('-', '_').strip()
    id_tag_movie = name + '_' + date

    try:
        query = sql.SQL("INSERT INTO {table} ({fields}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)").format(
            table=sql.Identifier('movies'),
            fields=sql.SQL(',').join([
                sql.Identifier('tag'),
                sql.Identifier('movie_title'),
                sql.Identifier('original_title'),
                sql.Identifier('release_date'),
                sql.Identifier('runtime'),
                sql.Identifier('status'),
                sql.Identifier('audience_rating'),
                sql.Identifier('num_ratings')
            ])

        )
        cursor.execute(query, (id_tag_movie, details["title"], details["original_title"], details["release_date"],
                               details["runtime"], details["status"], details["vote_average"], details["vote_count"]))

    except psycopg2.DatabaseError as e:
        print("Movie Duplicate")
        return

    """
    --------------------------------------------------------------------------------------------------------------------
        GET MOVIE GENRES AND LINK TO MOVIES
    --------------------------------------------------------------------------------------------------------------------
    """
    for genre in details["genres"]:
        try:
            query = sql.SQL("INSERT INTO {table} ({col1}) VALUES (%s)").format(
                table=sql.Identifier('genres'),
                col1=sql.Identifier('genre_name')
            )
            cursor.execute(query, (genre["name"],))
        except psycopg2.DatabaseError as e:
            # Expected
            pass

        try:
            query = sql.SQL("INSERT INTO {insert_table} ({insert_value1}, {insert_value2}) "
                            "VALUES ("
                            "(SELECT {query_column1} FROM {query_table1} WHERE {query_cond1} = %s), "
                            "(SELECT {query_column2} FROM {query_table2} WHERE {query_cond2} = %s))").format(
                insert_table=sql.Identifier('movie_genres'),
                insert_value1=sql.Identifier('movie_id'),
                insert_value2=sql.Identifier('genre_id'),
                query_column1=sql.Identifier("movie_id"),
                query_table1=sql.Identifier("movies"),
                query_cond1=sql.Identifier("tag"),
                query_column2=sql.Identifier("genre_id"),
                query_table2=sql.Identifier("genres"),
                query_cond2=sql.Identifier("genre_name")
            )
            cursor.execute(query, (id_tag_movie, genre["name"]))
        except psycopg2.DatabaseError as e:
            print("something went wrong: ", e)
    response.close()
    """
    --------------------------------------------------------------------------------------------------------------------
        GET ALL OF THE PEOPLE DETAILS
    --------------------------------------------------------------------------------------------------------------------
    """
    credit_reaper(url=url,
                  headers=headers,
                  cursor=cursor,
                  media='movie',
                  parent_tag=id_tag_movie)
    """
    --------------------------------------------------------------------------------------------------------------------
    GET ALL OF THE MOVIE REVIEWS
    --------------------------------------------------------------------------------------------------------------------
    """
    reviews_url = url + "/reviews"
    response = requests.get(url=reviews_url, headers=headers)
    reviews_TMDB = response.json()

    for review in reviews_TMDB["results"]:
        response_review = requests.get(url="https://api.themoviedb.org/3/review/" + str(review["id"]), headers=headers)

        details = response_review.json()
        name = details["author_details"]["username"].replace(' ', '_').lower().strip()
        name = re.sub(r'\W+', '', name)
        title = details["media_title"].replace('-', '_').lower().strip()
        title = re.sub(r'\W+', '', title)
        id_tag_review = name + '_' + title
        try:
            query = sql.SQL("INSERT INTO {table} ({fields}) "
                            "VALUES ("
                            "(SELECT {query_col1} FROM {query_table1} WHERE {query_cond1} = %s), "
                            "%s, %s, %s, %s, %s, %s, %s, %s, %s)").format(
                table=sql.Identifier('movie_reviews'),
                fields=sql.SQL(',').join([
                    sql.Identifier('movie_id'),
                    sql.Identifier('tag'),
                    sql.Identifier('author_name'),
                    sql.Identifier('author_username'),
                    sql.Identifier('rating'),
                    sql.Identifier('content'),
                    sql.Identifier('time_created'),
                    sql.Identifier('time_updated'),
                    sql.Identifier('origin'),
                    sql.Identifier('reference')
                ]),
                query_col1=sql.Identifier('movie_id'),
                query_table1=sql.Identifier('movies'),
                query_cond1=sql.Identifier('tag')

            )
            cursor.execute(query, (id_tag_movie, id_tag_review, details["author_details"]["name"],
                                   details["author_details"]["username"], details["author_details"]["rating"],
                                   details["content"], details["created_at"], details["updated_at"], 'TMDB',
                                   details["url"]))

        except psycopg2.DatabaseError as e:
            print("Duplicate Review")
    response.close()
    """
    --------------------------------------------------------------------------------------------------------------------
    GET ALL OF THE MOVIE PROVIDERS
    --------------------------------------------------------------------------------------------------------------------
    """
    providers_url = url + "/watch/providers"
    response = requests.get(url=providers_url, headers=headers)
    watch = response.json()

    for iso in watch["results"].keys():

        # In the future, regions will most likely be entered ahead of time
        try:
            query = sql.SQL("INSERT INTO {table} ({fields}) "
                            "VALUES (%s)").format(
                table=sql.Identifier('regions'),
                fields=sql.SQL(',').join([
                    sql.Identifier('iso')
                ])
            )
            cursor.execute(query, (iso, ))
        except psycopg2.DatabaseError as e:
            pass

        region = watch["results"][iso]
        provider_info = {}
        if "rent" in region.keys():
            provider_purchase_formatting(region, cursor, provider_info, "rent")

        if "buy" in region.keys():
            provider_purchase_formatting(region, cursor, provider_info, "buy")

        if "flatrate" in region.keys():
            provider_purchase_formatting(region, cursor, provider_info, "flatrate")

        for provider in provider_info.keys():

            purchase_info = provider_info[provider]
            try:
                query = sql.SQL("INSERT INTO {table} ({fields}) "
                                "VALUES ("
                                "(SELECT {query_col1} FROM {query_table1} WHERE {query_cond1} = %s), "
                                "(SELECT {query_col2} FROM {query_table2} WHERE {query_cond2} = %s), "
                                "(SELECT {query_col3} FROM {query_table3} WHERE {query_cond3} = %s), "
                                "%s, %s, %s, %s, %s, %s)").format(
                    table=sql.Identifier('region_provided_movies'),
                    fields=sql.SQL(',').join([
                        sql.Identifier('movie_id'),
                        sql.Identifier('region_id'),
                        sql.Identifier('provider_id'),
                        sql.Identifier('rent'),
                        sql.Identifier('rent_price'),
                        sql.Identifier('buy'),
                        sql.Identifier('buy_price'),
                        sql.Identifier('flatrate'),
                        sql.Identifier('flatrate_price'),
                    ]),
                    query_col1=sql.Identifier('movie_id'),
                    query_table1=sql.Identifier('movies'),
                    query_cond1=sql.Identifier('tag'),
                    query_col2=sql.Identifier('region_id'),
                    query_table2=sql.Identifier('regions'),
                    query_cond2=sql.Identifier('iso'),
                    query_col3=sql.Identifier('provider_id'),
                    query_table3=sql.Identifier('providers'),
                    query_cond3=sql.Identifier('provider_name')

                )
                cursor.execute(query, (id_tag_movie, iso, provider, purchase_info["rent"], None,
                                       purchase_info["buy"], None, purchase_info["flatrate"], None))
            except psycopg2.DatabaseError as e:
                print("Something went wrong: ", e)

    response.close()


def provider_purchase_formatting(region: dict, cursor: any, provider_info: dict, purchase_type: str):
    for provider in region[purchase_type]:
        try:
            query = sql.SQL("INSERT INTO {table} ({fields}) "
                            "VALUES (%s)").format(
                table=sql.Identifier('providers'),
                fields=sql.SQL(',').join([
                    sql.Identifier('provider_name')
                ])
            )
            cursor.execute(query, (provider["provider_name"],))
        except psycopg2.DatabaseError as e:
            pass
        if provider["provider_name"] in provider_info.keys():
            provider_info[provider["provider_name"]][purchase_type] = True
        else:
            if purchase_type == "rent":
                provider_info[provider["provider_name"]] = {"rent": True, "buy": False, "flatrate": False}
            elif purchase_type == "buy":
                provider_info[provider["provider_name"]] = {"rent": False, "buy": True, "flatrate": False}
            else:
                provider_info[provider["provider_name"]] = {"rent": False, "buy": False, "flatrate": True}


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
