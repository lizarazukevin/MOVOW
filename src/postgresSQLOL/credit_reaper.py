import psycopg2
import requests
from psycopg2 import sql


def credit_reaper(url: str, headers: dict, cursor: any, media: str, parent_tag: str):
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
            print("Duplicate Person: ", details["name"])

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
                table=sql.Identifier((media + '_casting_credits')),
                fields=sql.SQL(',').join([
                    sql.Identifier((media + '_id')),
                    sql.Identifier('person_id'),
                    sql.Identifier('character'),
                ]),
                query_col1=sql.Identifier((media + '_id')),
                query_table1=sql.Identifier((media + 's')),
                query_cond1=sql.Identifier('tag'),
                query_col2=sql.Identifier('person_id'),
                query_table2=sql.Identifier('people'),
                query_cond2=sql.Identifier('tag'),
            )
            cursor.execute(query, (parent_tag, id_tag_person, person["character"]))
        except psycopg2.DatabaseError as e:
            print("Something went wrong: ", e)

    """
    --------------------------------------------------------------------------------------------------------------------
        GET ALL OF THE CREW DETAILS
    --------------------------------------------------------------------------------------------------------------------
    """
    for person in people["crew"]:
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
            print("Duplicate Person: ", details["name"])

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
                table=sql.Identifier((media + '_crew_credits')),
                fields=sql.SQL(',').join([
                    sql.Identifier((media + '_id')),
                    sql.Identifier('person_id'),
                    sql.Identifier('department'),
                    sql.Identifier('job')
                ]),
                query_col1=sql.Identifier((media + '_id')),
                query_table1=sql.Identifier((media + 's')),
                query_cond1=sql.Identifier('tag'),
                query_col2=sql.Identifier('person_id'),
                query_table2=sql.Identifier('people'),
                query_cond2=sql.Identifier('tag'),
            )
            cursor.execute(query, (parent_tag, id_tag_person, person["department"], person["job"]))
        except psycopg2.DatabaseError as e:
            print("Something went wrong: ", e)

    response.close()
