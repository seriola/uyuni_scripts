#!/usr/bin/python3

import argparse
import psycopg2
import re

def db_connect():
    db = 'uyuni'
    dbhost = '127.0.0.1'
    dbport = '5432'
    dbuser = 'YOUR USERNAME'
    dbpwd = 'YOUR PASSWORD'


    # Establishing the connection
    conn = psycopg2.connect(
        database=db, user=dbuser, password=dbpwd, host=dbhost, port=dbport
    )

    # Setting auto commit false
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    return(conn, cursor)

def db_close(conn):
    # Closing the connection
    conn.close()
    

def query_db(cursor, action_id, verbose):

    # query id in public.rhnactionapplystates using action_id
    cursor.execute("SELECT * FROM public.rhnactionapplystates WHERE action_id = " + str(action_id))
    result = cursor.fetchone();

    if result:
        states_id = result[0]

        if verbose == True:
            print("State:")
            print("------")
            print("id:                     ", result[0])
            print("action_id:              ", result[1])
            print("states:                 ", result[2])
            print("test:                   ", result[3])
            print("created:                ", result[4])
            print("modified:               ", result[5])
            print("")
    else:
        print("No Action found. Check your action_id.")
        return 1

    # query state output using states_id 
    cursor.execute("SELECT * from public.rhnactionapplystatesresult WHERE action_apply_states_id = " + str(states_id))

    # fetching first row
    result = cursor.fetchone();

    if result:
        if verbose == True:
            print("State result:")
            print("-------------")
            print("id:                     ", result[0])
            print("action_apply_states_id: ", result[1])
            print("return_code:            ", result[3])
            print("output:                 ", re.sub(r"\\n", "\n", str(bytes(result[2]))))
            print("")
        else:
            mystring = re.sub(r"\\n", "\n", str(bytes(result[2])))
            print(mystring)
    else:
        print("No result found.")


def check_args():
    parser = argparse.ArgumentParser(description="Action ID (integer)")

    parser.add_argument('-id', '--action_id', required=True, type=int, help='ID of state action')
    parser.add_argument("-v", "--verbose", help="verbose output", action = "store_true")

    args = parser.parse_args()

    return(args)


if __name__ == "__main__":
    args = check_args()

    if args.verbose:
        verbose = True
    else:
        verbose = False

    conn, cursor = db_connect()

    query_db(cursor, int(args.action_id), verbose)

    db_close(conn)
