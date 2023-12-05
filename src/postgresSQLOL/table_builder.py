import psycopg2
from config import config
import argparse
import media_tables
import user_tables


def create_tables(commands):
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser("movie trotter")
    parser.add_argument("group", help="The group of tables to build")
    args = parser.parse_args()

    if args.group == "media":
        cmds = media_tables.commands
    elif args.group == "user":
        cmds = user_tables.commands
    create_tables(cmds)
