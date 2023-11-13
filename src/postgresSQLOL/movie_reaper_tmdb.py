from time import sleep
import argparse
import sys
import psycopg2
from config import config
import requests
import re
from psycopg2 import sql


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
        GET ALL OF THE CAST DETAILS
    --------------------------------------------------------------------------------------------------------------------
    """
    credits_url = url + "/credits"
    response = requests.get(url=credits_url, headers=headers)
    people = response.json()
    for person in people["cast"]:
        response_person = requests.get(url="https://api.themoviedb.org/3/person/" + str(person["id"]), headers=headers)

        details = response_person.json()

        name = details["name"].replace(' ', '_').lower().strip()
        try:
            birth = details["birthday"].replace('-', '_').strip()
        except AttributeError:
            birth = "0000_00_00"
        id_tag_person = name + '_' + birth
        try:
            query = sql.SQL("INSERT INTO {table} ({fields}) VALUES (%s, %s, %s, %s, %s, %s)").format(
                table=sql.Identifier('people'),
                fields=sql.SQL(',').join([
                    sql.Identifier('tag'),
                    sql.Identifier('person_name'),
                    sql.Identifier('birthday'),
                    sql.Identifier('death'),
                    sql.Identifier('gender'),
                    sql.Identifier('department'),
                ])

            )
            cursor.execute(query, (id_tag_person, details["name"], details["birthday"], details["deathday"],
                                   details["gender"], details["known_for_department"]))

        except psycopg2.DatabaseError as e:
            print("Duplicate Person")

        for alias in details["also_known_as"]:
            try:
                query = sql.SQL("INSERT INTO {table} ({fields}) "
                                "VALUES ("
                                "(SELECT {query_col} FROM {query_table} WHERE {query_cond} = %s), "
                                "%s)").format(
                    table=sql.Identifier('people_aliases'),
                    fields=sql.SQL(',').join([
                        sql.Identifier('person_id'),
                        sql.Identifier('name')
                    ]),
                    query_col=sql.Identifier('person_id'),
                    query_table=sql.Identifier('people'),
                    query_cond=sql.Identifier('tag')
                )
                cursor.execute(query, (id_tag_person, alias))
            except psycopg2.DatabaseError as e:
                print("Something went wrong: ", e)
        """
        --------------------------------------------------------------------------------------------------------------------
            GET ALL OF THE CAST EXPERIENCES/CREDITS
        --------------------------------------------------------------------------------------------------------------------
        """
        try:
            query = sql.SQL("INSERT INTO {table} ({fields}) "
                            "VALUES ("
                            "(SELECT {query_col1} FROM {query_table1} WHERE {query_cond1} = %s), "
                            "(SELECT {query_col2} FROM {query_table2} WHERE {query_cond2} = %s), "
                            "%s)").format(
                table=sql.Identifier('movie_casting_credits'),
                fields=sql.SQL(',').join([
                    sql.Identifier('movie_id'),
                    sql.Identifier('person_id'),
                    sql.Identifier('character'),
                ]),
                query_col1=sql.Identifier('movie_id'),
                query_table1=sql.Identifier('movies'),
                query_cond1=sql.Identifier('tag'),
                query_col2=sql.Identifier('person_id'),
                query_table2=sql.Identifier('people'),
                query_cond2=sql.Identifier('tag'),
            )
            cursor.execute(query, (id_tag_movie, id_tag_person, person["character"]))
        except psycopg2.DatabaseError as e:
            print("Something went wrong: ", e)

    """
    --------------------------------------------------------------------------------------------------------------------
        GET ALL OF THE CREW DETAILS
    --------------------------------------------------------------------------------------------------------------------
    """
    for person in people["cast"]:
        response_person = requests.get(url="https://api.themoviedb.org/3/person/" + str(person["id"]), headers=headers)

        details = response_person.json()

        name = details["name"].replace(' ', '_').lower().strip()
        try:
            birth = details["birthday"].replace('-', '_').strip()
        except AttributeError:
            birth = "0000_00_00"
        id_tag_person = name + '_' + birth
        try:
            query = sql.SQL("INSERT INTO {table} ({fields}) VALUES (%s, %s, %s, %s, %s, %s)").format(
                table=sql.Identifier('people'),
                fields=sql.SQL(',').join([
                    sql.Identifier('tag'),
                    sql.Identifier('person_name'),
                    sql.Identifier('birthday'),
                    sql.Identifier('death'),
                    sql.Identifier('gender'),
                    sql.Identifier('department'),
                ])

            )
            cursor.execute(query, (id_tag_person, details["name"], details["birthday"], details["deathday"],
                                   details["gender"], details["known_for_department"]))

        except psycopg2.DatabaseError as e:
            print("Duplicate Person")

        for alias in details["also_known_as"]:
            try:
                query = sql.SQL("INSERT INTO {table} ({fields}) "
                                "VALUES ("
                                "(SELECT {query_col} FROM {query_table} WHERE {query_cond} = %s), "
                                "%s)").format(
                    table=sql.Identifier('people_aliases'),
                    fields=sql.SQL(',').join([
                        sql.Identifier('person_id'),
                        sql.Identifier('name')
                    ]),
                    query_col=sql.Identifier('person_id'),
                    query_table=sql.Identifier('people'),
                    query_cond=sql.Identifier('tag')
                )
                cursor.execute(query, (id_tag_person, alias))
            except psycopg2.DatabaseError as e:
                print("Something went wrong: ", e)
        """
        --------------------------------------------------------------------------------------------------------------------
            GET ALL OF THE CREW EXPERIENCES/CREDITS
        --------------------------------------------------------------------------------------------------------------------
        """
        try:
            query = sql.SQL("INSERT INTO {table} ({fields}) "
                            "VALUES ("
                            "(SELECT {query_col1} FROM {query_table1} WHERE {query_cond1} = %s), "
                            "(SELECT {query_col2} FROM {query_table2} WHERE {query_cond2} = %s), "
                            "%s, "
                            "%s)").format(
                table=sql.Identifier('movie_crew_credits'),
                fields=sql.SQL(',').join([
                    sql.Identifier('movie_id'),
                    sql.Identifier('person_id'),
                    sql.Identifier('department'),
                    sql.Identifier('job')
                ]),
                query_col1=sql.Identifier('movie_id'),
                query_table1=sql.Identifier('movies'),
                query_cond1=sql.Identifier('tag'),
                query_col2=sql.Identifier('person_id'),
                query_table2=sql.Identifier('people'),
                query_cond2=sql.Identifier('tag'),
            )
            cursor.execute(query, (id_tag_movie, id_tag_person, person["department"], person["job"]))
        except psycopg2.DatabaseError as e:
            print("Something went wrong: ", e)

    response.close()
    """
    --------------------------------------------------------------------------------------------------------------------
    GET ALL OF THE MOVIE REVIEWS
    --------------------------------------------------------------------------------------------------------------------
    """


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
