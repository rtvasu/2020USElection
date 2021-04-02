import mysql.connector
from mysql.connector import errorcode
import locale
import getpass
from electionDB import electionDB


import os

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

"""
    Conf
"""
username = input("Username: ")
password = getpass.getpass(prompt='Password: ', stream=None)

config = {
    'user': username,  # insert your user name here
    'password': password,  # insert your password here
    'host': 'marmoset04.shoshin.uwaterloo.ca',
    'database': 'project_1',
    'raise_on_warnings': True
}

# error checking
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

    while (1):

        print(
            "------------------------------- Welcome to the 2020 election database system -------------------------------")
        print("\n")


        #Main Screen
        print("What do you want to do?")
        print("(S) Get statistics")
        print("(I) Insert Data")
        print("(D) Data Mine")
        print("\n")

        command = input ("Your command: ")
        print("\n")

        if (command == 's'):


            while (1):

                print("............................................................................................ ...")
                print ("Welcome to search. These are the actions you can do. Please choose one of them: ")

                print("(1) Voting results for a state")
                print("(2) Voting results for all states")
                print("(3) Voting results for a county")
                print("(4) Voting results for all counties in a state")
                print("(5) Get the most popular tweets from a state")
                print("(6) Demographics of a state")
                print("(7) Demographics of a county")
                print("( ANY KEY ) Exit")
                print("\n")
                command_s = input("Your command: ")
                print("\n")

                if (command_s == '1'):

                    print("(1) Voting results for a state")
                    print("\n")
                    stateInput = input("Please enter a state: ")
                    print("\n")

                    totalVotes = results.totalVotesByState(stateInput)
                    if (not totalVotes):
                        print("Please try again.")
                        print("\n")
                    else:
                        for i in totalVotes:
                            state = locale.format_string("%s", i[0], grouping=True)
                            votes = locale.format_string("%d", i[1], grouping=True)
                            print("The total votes in ", state, " is ", votes, " votes.")
                        print("\n")


                elif (command_s == '2'):

                    print("(2) Voting results for all states")
                    print("\n")

                    totalVotes = results.totalVotesByState('A')
                    if (not totalVotes):
                        print("Please try again.")
                        print("\n")
                    else:
                        for i in totalVotes:
                            state = locale.format_string("%s", i[0], grouping=True)
                            votes = locale.format_string("%d", i[1], grouping=True)
                            print("The total votes in ", state, " is ", votes, " votes.")
                        print("\n")



                elif (command_s == '3'):
                    print("(3) Voting results for a county")
                    print("\n")
                    askState = input("Which state? ")
                    print("\n")
                    stateList = results.getListioCountiesUnderState(askState)
                    if (not stateList):
                        print("Please try again.")
                        print("\n")
                    else:
                        for i in stateList:
                            print(i[0])
                        print("\n")

                        county = input(
                            "Here is a list of counties in this state. Please choose a county to view results for: ")
                        countyResults = results.totalVotesByCounty(askState, county)

                        if (not countyResults):
                            print("Please try again.")
                            print("\n")
                        else:
                            for i in countyResults:
                                votes = locale.format_string("%d", i[2], grouping=True)
                                print("The total votes in ", county, " is ", votes, " votes.")
                            print("\n")



                elif (command_s == '4'):
                    print("(4) Voting results for all counties in a state")
                    print("\n")
                    askState = input("Which state? ")
                    print("\n")
                    stateList = results.getListioCountiesUnderState(askState)
                    if (not stateList):
                        print("Please try again.")
                        print("\n")
                    else:
                        countyResults = results.totalVotesByCounty(askState, 'A')

                        if (not countyResults):
                            print("Please try again.")
                            print("\n")
                        else:
                            for i in countyResults:
                                county = locale.format_string("%s", i[1], grouping=True)
                                votes = locale.format_string("%d", i[2], grouping=True)
                                print("The total votes in ", county, " is ", votes, " votes.")
                            print("\n")





                elif (command_s == '5'):
                    print("(5) Get the most popular tweets from a state")
                    print("\n")
                    stateInput = input("Please enter a state: ")
                    print("\n")
                    numberOfTweets = input("How many tweets do you want to view? ")
                    print("\n")

                    bidenTweets = results.tweetsBiden(stateInput, numberOfTweets)
                    if (not bidenTweets):
                        print("Please try again.")
                        print("\n")
                    else:
                        print ("Most popular tweets under #TweetsBiden for %s:" % stateInput)
                        for i in bidenTweets:
                            tweet = locale.format_string("%s", i[2], grouping=True)
                            likes = locale.format_string("%d", i[3], grouping=True)
                            retweets = locale.format_string("%d", i[4], grouping=True)
                            print(" - " + tweet)
                            print("(Likes: " + likes + ", Retweets: ", retweets + ")")
                            print("\n")
                        print("\n")

                    print("--------------------------------------------------------------------------")

                    trumpTweets = results.tweetsTrump(stateInput, numberOfTweets)
                    if (not trumpTweets):
                        print("Please try again.")
                        print("\n")
                    else:
                        print("Most popular tweets under #TweetsTrump for %s:" % stateInput)
                        for i in trumpTweets:
                            tweet = locale.format_string("%s", i[2], grouping=True)
                            likes = locale.format_string("%d", i[3], grouping=True)
                            retweets = locale.format_string("%d", i[4], grouping=True)
                            print(" - " + tweet)
                            print("(Likes: " + likes + ", Retweets: ", retweets + ")")
                            print("\n")
                        print("\n")


                elif (command_s == '6'):
                    print("(6) Demographics of a state")
                    print("\n")
                    state = input("To search for a particular state, enter a state: ")
                    print("\n")
                    demographics = results.demographicsByState(state)

                    if (not demographics):
                        print("Please try again.")
                        print("\n")
                    else:
                        for i in demographics:
                            print("-- ", locale.format_string("%s", i[0], grouping=True), " Demographics --")
                            print("Total Population - ", locale.format_string("%d", i[1], grouping=True))
                            print("Men - ", locale.format_string("%s", i[2], grouping=True), "%")
                            print("Women - ", locale.format_string("%s", i[3], grouping=True), "%")
                            print("White - ", locale.format_string("%s", i[4], grouping=True), "%")
                            print("Black - ", locale.format_string("%s", i[5], grouping=True), "%")
                            print("Hispanic - ", locale.format_string("%s", i[6], grouping=True), "%")
                            print("Asian - ", locale.format_string("%s", i[7], grouping=True), "%")
                            print("Native - ", locale.format_string("%s", i[8], grouping=True), "%")
                        print("\n")


                elif (command_s == '7'):
                    print("(7) Demographics of a county")
                    print("\n")
                    askState = input("Which state? ")
                    stateList = results.getListioCountiesUnderState(askState)
                    if (not stateList):
                        print("Please try again.")
                        print("\n")
                    else:
                        for i in stateList:
                            print(i[0])
                        print("\n")

                        county = input(
                            "Here is a list of counties in this state. Please choose a county to view results for: ")
                        demographics = results.demographicsByCounty(askState, county)

                        if (not demographics):
                            print("Please try again.")
                            print("\n")
                        else:
                            for i in demographics:
                                print("-- ", locale.format_string("%s", i[1], grouping=True), " Demographics --")
                                print("Total Population - ", locale.format_string("%d", i[2], grouping=True))
                                print("Men - ", locale.format_string("%s", i[3], grouping=True), "%")
                                print("Women - ", locale.format_string("%s", i[4], grouping=True), "%")
                                print("White - ", locale.format_string("%s", i[5], grouping=True), "%")
                                print("Black - ", locale.format_string("%s", i[6], grouping=True), "%")
                                print("Hispanic - ", locale.format_string("%s", i[7], grouping=True), "%")
                                print("Asian - ", locale.format_string("%s", i[8], grouping=True), "%")
                                print("Native - ", locale.format_string("%s", i[9], grouping=True), "%")
                            print("\n")
                else:
                    print("Thank you!")
                    break

        elif (command == 'i'):
            print("Insertion coming soon")
            print("\n")


        elif (command == 'd'):
            print("Data Mining coming soon")
            print("\n")

    # remember to close connection
    cursor.close()
    cnx.close()