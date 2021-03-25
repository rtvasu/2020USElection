import mysql.connector
from mysql.connector import errorcode
import locale
import decimal
import fire
import getpass
import sys
from electionDB import electionDB

"""
    Conf
"""
username = input("Username: ")
password = getpass.getpass(prompt='Password: ', stream=None)

config = {
    'user':username,#insert your user name here
    'password':password,#insert your password here
    'host':'marmoset04.shoshin.uwaterloo.ca',
    'database':'project_1',
    'raise_on_warnings':True
}

#error checking
try:
    cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:



    """
        Configure DB Object
    """
    cursor = cnx.cursor()
    results = electionDB(cursor)


    """
        MAIN
    """
    print("............................Welcome to the 2020 election database system............................")
    print("\n")

    # FIND VOTES BY a particular state
    state = input("Please enter any state. To get a full list of votes per state, press A: ")

    totalVotes = results.totalVotesByState(state)
    for i in totalVotes:
        state = locale.format_string("%s", i[0], grouping=True)
        votes = locale.format_string("%d", i[1], grouping=True)
        print("The total votes in ", state, " is ", votes, " votes.")
    print("\n")


    # FIND demographics for a county/state
    state = input("Demographics. To search for a particular state, enter a state, press A: ")

    demographics = results.demographicsByState(state)
    for i in demographics:
        print("-- ", locale.format_string("%s", i[0], grouping=True), " Demographics --")
        print("Total Population - ", locale.format_string("%d", i[1], grouping=True))
        print("White - ", locale.format_string("%d", i[2], grouping=True), "%")
        print("Black - ", locale.format_string("%d", i[3], grouping=True), "%")
        print("Hispanic - ", locale.format_string("%d", i[4], grouping=True), "%")
        print("Asian - ", locale.format_string("%d", i[5], grouping=True), "%")
        print("Native - ", locale.format_string("%d", i[6], grouping=True), "%")
        print("Pacific - ", locale.format_string("%d", i[7], grouping=True), "%")
        print("\n")


    # remember to close connection
    cursor.close()
    cnx.close()