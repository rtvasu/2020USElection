"""
    LIBRARIES
"""
import mysql.connector
from mysql.connector import errorcode
import locale
import getpass
from electionDB import electionDB
# from os import system, name
# import os
# import string
# import time
# import pyfiglet


# def cls():
#     os.system('cls' if os.name == 'nt' else 'clear')

"""
    CONFIGURATION
"""
print("..........................................................................................")
username = input("Username: ")
password = getpass.getpass(prompt='Password: ', stream=None)

config = {
    'user': username,  # insert your user name here
    'password': password,  # insert your password here
    'host': 'marmoset04.shoshin.uwaterloo.ca',
    'database': 'project_1',
    'raise_on_warnings': True
}

"""
    CONNECTING TO MYSQL SERVER
"""
try:
    cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Error: Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Error: Database does not exist")
    else:
        print(err)
else:

    """
        CONFIGURE DB OBJECT
    """
    cursor = cnx.cursor()
    results = electionDB(cursor, cnx)

    """
        MAIN
    """
    print("..........................................................................................")
    print("..........................................................................................")
    print("......................... WELCOME TO 2020 ELECTION DATABASE ..............................")
    print("..........................................................................................")
    print("..........................................................................................")
    print("\n")

    while 1:
        """
        MAIN VARIABLES
        """
        continue1 = continue2 = continue3 = continue4 = continue5 = continue6 = continue7 = continue8 = continue9 = 1

        # cls()
        # Main Screen
        print("Please select an option and enter the number:")
        print("[1] Get statistics")
        print("[2] Insert Data")
        print("[3] Data Mine")
        print("[4] Exit")
        print("\n")

        command = input("Your selection: ")
        print("\n")
        # cls()

        if command.lower() == '1':

            while 1:
                continue1 = 1
                print("..........................................................................................")
                print("......................................... WHAT STATS WOULD YOU LIKE TO SEE? .........................................")
                print("..........................................................................................")
                print("\n")

                print("Please select an option and enter the number: ")
                print("[1] Voting results for a state")
                print("[2] Voting results for all states")
                print("[3] Voting results for a county")
                print("[4] Voting results for all counties in a state")
                print("[5] Get the most popular tweets from a state")
                print("[6] Demographics of a state")
                print("[7] Demographics of a county")
                print("[ANY KEY] Exit")
                print("\n")

                command_s = input("Your command: ")
                print("\n")
                # cls()

                # (1) Voting results for a state
                if command_s.lower() == '1':
                    print("..........................................................................................")
                    print("............................... VOTING RESULTS FOR A STATE ...............................")
                    print("..........................................................................................")
                    print("\n")

                    while continue1 == 1:
                        stateInput = input("Please enter name of state: ")

                        # FETCH RESULTS
                        totalVotes = results.totalVotesByState(stateInput)
                        totalResults = results.votingResultsbyPartybyState(stateInput, 1, 1)

                        # IF ERROR, TRY AGAIN
                        if (not totalVotes) or (not totalResults):
                            print("Error: Check if state exists and is spelled correctly.\n")
                        elif (totalVotes == -1 or totalResults == -1):
                            exit()

                        # DISPLAY RESULTS
                        else:
                            for i in totalVotes:
                                state = locale.format_string("%s", i[0], grouping=True)
                                votes_total = locale.format_string("%d", i[1], grouping=True)

                            for i in totalResults:
                                party = locale.format_string("%s", i[1], grouping=True)
                                votes = locale.format_string("%d", i[2], grouping=True)
                                print("The winning party in ", state, " is ", party,
                                      " with " + votes + " votes & the total votes  is ", votes_total)
                            print("\n")

                        # ASK TO CONTINUE
                        while(1):
                            yn = input("Continue? Y/N: ")
                            if yn == 'y':
                                continue1 = 1
                                break
                            elif yn == 'n':
                                continue1 = 0
                                break
                            else:
                                print("Error: Please enter valid input.\n")
                        # cls()



                elif command_s.lower() == '2':

                    print("..........................................................................................")
                    print("............................. VOTING RESULTS FOR ALL STATES ..............................")
                    print("..........................................................................................")
                    print("\n")

                    while continue2 == 1:
                        totalVotes = results.totalVotesByState('a')
                        totalResults = results.votingResultsbyPartybyState('a', 1, 0)
                        if not totalVotes:
                            print("Please try again.")
                            print("\n")
                        elif(totalVotes == -1 or totalResults == -1):
                            exit()
                        else:
                            for i in totalVotes:
                                votes_total = locale.format_string("%d", i[1], grouping=True)

                            for i in totalResults:
                                state = locale.format_string("%s", i[0], grouping=True)
                                party = locale.format_string("%s", i[1], grouping=True)
                                votes = locale.format_string("%d", i[2], grouping=True)
                                print("The winning party in ", state, " is ", party,
                                      " with " + votes + " votes & the total votes  is ", votes_total)
                            print("\n")

                        # ask if I can continue
                        while(1):
                            yn = input("Continue? Y/N: ")
                            if yn == 'y':
                                continue2 = 1
                                break
                            elif yn == 'n':
                                continue2 = 0
                                break
                            else:
                                print("Error: Please enter valid input.\n")
                        # cls()
                        print("\n")



                elif command_s.lower() == '3':
                    print("..........................................................................................")
                    print(".........................,.... VOTING RESULTS FOR A COUNTY ...............................")
                    print("..........................................................................................")
                    print("\n")

                    while continue3 == 1:
                        askState = input("Which state? ")
                        print("\n")
                        stateList = results.getListioCountiesUnderState(askState)
                        if not stateList:
                            print("Please try again.")
                            print("\n")
                        elif(stateList == -1):
                            exit()
                        else:
                            for i in stateList:
                                print(i[0])
                            print("\n")

                            county = input("Here is a list of counties in this state. Please choose a county to view results for: ")
                            countyTotalResults = results.totalVotesByCounty(askState, county)
                            countyVotingResults = results.votingResultsbyPartybyCounty(askState, county, 1)

                            if not countyTotalResults:
                                print("Please try again.")
                                print("\n")
                            elif countyTotalResults == -1 or countyVotingResults == -1:
                                exit()
                            else:
                                for i in countyTotalResults:
                                    total_votes = locale.format_string("%d", i[2], grouping=True)

                                for i in countyVotingResults:
                                    county = locale.format_string("%s", i[1], grouping=True)
                                    party = locale.format_string("%s", i[2], grouping=True)
                                    votes = locale.format_string("%d", i[3], grouping=True)
                                    print("The winning party in ", county, " is ", party,
                                          " with " + votes + " votes & the total votes  is ", total_votes)
                                print("\n")

                            # ask if I can continue
                            while 1:
                                yn = input("Continue? Y/N: ")
                                if yn == 'y':
                                    continue3 = 1
                                    break
                                elif yn == 'n':
                                    continue3 = 0
                                    break
                                else:
                                    print("Error: Please enter valid input.\n")
                            # cls()
                            print("\n")



                elif command_s.lower() == '4':
                    print("..........................................................................................")
                    print("...................... VOTING RESULTS FOR ALL COUNTIES IN A STATE ........................")
                    print("..........................................................................................")
                    print("\n")

                    while continue4 == 1:
                        askState = input("Which state? ")
                        print("\n")
                        stateList = results.getListioCountiesUnderState(askState)
                        if not stateList:
                            print("Please try again.")
                            print("\n")
                        elif(stateList == -1):
                            exit()
                        else:
                            countyTotalVotes = results.totalVotesByCounty(askState, 'A')
                            countyVotingResults = results.votingResultsbyPartybyCounty(askState, 'A', 1)

                            if not countyTotalVotes:
                                print("Please try again.")
                                print("\n")
                            elif countyTotalVotes == -1 or countyVotingResults == -1:
                                exit()
                            else:
                                for i in countyTotalVotes:
                                    total_votes = locale.format_string("%d", i[2], grouping=True)

                                for i in countyVotingResults:
                                    county = locale.format_string("%s", i[1], grouping=True)
                                    party = locale.format_string("%s", i[2], grouping=True)
                                    votes = locale.format_string("%d", i[3], grouping=True)
                                    print("The winning party in ", county, " is ", party,
                                          " with " + votes + " votes & the total votes  is ", total_votes)
                                print("\n")

                            # ask if I can continue
                            while(1):
                                yn = input("Continue? Y/N: ")
                                if yn == 'y':
                                    continue4 = 1
                                    break
                                elif yn == 'n':
                                    continue4 = 0
                                    break
                                else:
                                    print("Error: Please enter valid input.\n")
                            # cls()
                            print("\n")


                elif command_s.lower() == '5':
                    print("..........................................................................................")
                    print(".............................. MOST POPULAR TWEETS IN STATE ..............................")
                    print("..........................................................................................")
                    print("\n")

                    while continue5 == 1:
                        stateInput = input("Please enter a state: ")
                        print("\n")

                        if not stateInput:
                            exit()
                        numberOfTweets = input("How many tweets do you want to view? ")
                        print("\n")

                        bidenTweets = results.tweetsBiden(stateInput, numberOfTweets)
                        if not bidenTweets:
                            print("Please try again.")
                            print("\n")
                        elif(bidenTweets == -1):
                            exit()
                        else:
                            print(
                                "..........................................................................................")
                            print(
                                "...................... MOST POPULAR TWEETS UNDER #TweetsBiden FOR %s ....................." % stateInput)
                            print(
                                "..........................................................................................")
                            for i in bidenTweets:
                                tweet = locale.format_string("%s", i[2], grouping=True)
                                likes = locale.format_string("%d", i[3], grouping=True)
                                retweets = locale.format_string("%d", i[4], grouping=True)
                                print(" - " + tweet)
                                print("(Likes: " + likes + ", Retweets: ", retweets + ")")
                            print("\n")

                        trumpTweets = results.tweetsTrump(stateInput, numberOfTweets)
                        if not trumpTweets:
                            print("Please try again.")
                            print("\n")
                        elif (trumpTweets == -1):
                            exit()
                        else:
                            print(
                                "..........................................................................................")
                            print(
                                "...................... MOST POPULAR TWEETS UNDER #TweetsTrump FOR %s ....................." % stateInput)
                            print(
                                "..........................................................................................")
                            for i in trumpTweets:
                                tweet = locale.format_string("%s", i[2], grouping=True)
                                likes = locale.format_string("%d", i[3], grouping=True)
                                retweets = locale.format_string("%d", i[4], grouping=True)
                                print(" - " + tweet)
                                print("(Likes: " + likes + ", Retweets: ", retweets + ")")
                            print("\n")

                        # ask if I can continue
                        while(1):
                            yn = input("Continue? Y/N: ")
                            if yn == 'y':
                                continue5 = 1
                                break
                            elif yn == 'n':
                                continue5 = 0
                                break
                            else:
                                print("Error: Please enter valid input.\n")
                        # cls()
                        print("\n")


                elif command_s.lower() == '6':
                    print("..........................................................................................")
                    print("................................. DEMOGRAPHICS OF A STATE ................................")
                    print("..........................................................................................")
                    print("\n")

                    while continue6 == 1:
                        state = input("To search for a particular state, enter a state: ")
                        print("\n")
                        demographics = results.demographicsByState(state)

                        if not demographics:
                            print("Please try again.")
                            print("\n")
                        elif (demographics == -1):
                            exit()
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

                        # ask if I can continue
                        while(1):
                            yn = input("Continue? Y/N: ")
                            if yn == 'y':
                                continue6 = 1
                                break
                            elif yn == 'n':
                                continue6 = 0
                                break
                            else:
                                print("Error: Please enter valid input.\n")
                        # cls()
                        print("\n")


                elif command_s.lower() == '7':
                    print("..........................................................................................")
                    print("................................. DEMOGRAPHICS OF A COUNTY ................................")
                    print("..........................................................................................")
                    print("\n")

                    while continue7 == 1:
                        askState = input("Which state? ")
                        stateList = results.getListioCountiesUnderState(askState)
                        if not stateList:
                            print("Please try again.\n")
                            continue
                        elif(stateList == -1):
                            exit()
                        else:
                            for i in stateList:
                                print(i[0])
                            print("\n")

                            county = input(
                                "Here is a list of counties in this state. Please choose a county to view results for: ")
                            demographics = results.demographicsByCounty(askState, county)

                            if not demographics:
                                print("Please try again.")
                                print("\n")
                            elif(demographics == -1):
                                exit()
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

                            # ask if I can continue
                            while(1):
                                yn = input("Continue? Y/N: ")
                                if yn == 'y':
                                    continue7 = 1
                                    break
                                elif yn == 'n':
                                    continue7 = 0
                                    break
                                else:
                                    print("Error: Please enter valid input.\n")
                            # cls()
                            print("\n")
                else:
                    print("Thank you!")
                    break

        elif command.lower() == '2':

            print("..........................................................................................")
            print(".................................. ADD YOUR COMMENT ......................................")
            print("..........................................................................................")
            print("\n")

            while continue8 == 1:
                # while(1):
                #     yn = input("Continue? Y/N: ")
                #     if yn == 'y':
                #         break
                #     elif yn == 'n':
                #         leave = 1
                #         break
                #     else:
                #         print("Error: Please enter valid input.\n")
                # # cls()
                # if (leave == 1):
                #     break
                #
                # if ee.lower() == 'n':
                #     break

                print("..........................................................................................")
                print("You can add any comment for a state or county")
                print("\n")
                state = input("Please enter a state: ")
                yn = input("Do you want to select a county? Y/N")
                print("\n")

                # Getting the county
                if yn.lower() == 'y':

                    # List of counties
                    stateList = results.getListioCountiesUnderState(state)
                    if not stateList:
                        print("Please try again.\n")
                        continue
                    elif stateList == -1:
                        exit()
                    else:
                        for i in stateList:
                            print("- " + i[0])
                    print("\n")

                    county = input("Please enter a county: ")
                    print("\n")

                    # Get the winning and losing votes
                    print("..........................................................................................")
                    print(".................................. CURRENT RESULTS .......................................")
                    print("..........................................................................................")
                    countyResults = results.votingResultsbyPartybyCounty(state, county, 0)

                    if not countyResults:
                        print("Sorry, no results available for this county. Please try again")
                        print("\n")
                    elif countyResults == -1:
                        exit()
                    else:
                        for i in countyResults:
                            party = locale.format_string("%s", i[2], grouping=True)
                            totalVotes = locale.format_string("%d", i[3], grouping=True)
                            print(party + " = " + totalVotes + " votes")
                        print("\n")

                        # insert data
                        party = input("State party from above list: ")
                        result = input("Enter comment for county: ")
                        success = results.addResults(state, county, party, result)
                        print("\n")

                        if success == 0:
                            print("Successfully added comment!")
                        elif success == -1:
                            exit()
                        else:
                            print("Sorry, try again")
                        print("\n")


                elif yn.lower() == 'n':
                    # Get the winning and losing votes
                    print("..........................................................................................")
                    print(".................................. CURRENT RESULTS .......................................")
                    print("..........................................................................................")

                    stateResults = results.votingResultsbyPartybyState(state, 0)

                    if not stateResults:
                        print("Sorry, no results available for this state. Please try again")
                        print("\n")
                    elif (stateResults == -1):
                        exit()
                    else:
                        for i in stateResults:
                            party = locale.format_string("%s", i[1], grouping=True)
                            totalVotes = locale.format_string("%d", i[2], grouping=True)
                            print(party + " = " + totalVotes + " votes")
                        print("\n")

                    # insert data
                    party = input("State party from above list: ")
                    result = input("Enter comment for state: ")
                    success = results.addResults(state, 0, party, result)

                    if success == 0:
                        print("Successfully added comment!")
                    elif success == -1:
                        exit()
                    else:
                        print("Sorry, try again")

                print("\n")
                while (1):
                    yn = input("Continue? Y/N: ")
                    if yn == 'y':
                        continue8 = 1
                        break
                    elif yn == 'n':
                        continue8 = 0
                        break
                    else:
                        print("Error: Please enter valid input.\n")



        elif command.lower() == '3':
            print("..........................................................................................")
            print(".................................. DATA MINING ......................................")
            print("..........................................................................................")

            print("\n")

            # while 1:
            # while(1):
            #     yn = input("Continue? Y/N: ")
            #     if yn == 'y':
            #         break
            #     elif yn == 'n':
            #         leave = 1
            #         break
            #     else:
            #         print("Error: Please enter valid input.\n")
            # # cls()
            # if (leave == 1):
            #     break

            while continue9 == 1:

                # if not stateList:
                #     print("Please try again.")
                #     print("\n")
                # elif(stateList == -1):
                #     exit()
                # else:
                #     for i in stateList:
                #         print(i[0])
                #     print("\n")
                #

                # GET THE DATA & GEENRATE THE CSV
                data = results.getData()
                if data == -1:
                    exit()

                # COMPUTE THE DATA
                testing = results.computeData()
                print("\n")

                # Results
                print(" Most important factors deciding the winning party:")
                print(testing)


                # CONTINUE??
                print("\n")
                while (1):
                    yn = input("Continue? Y/N: ")
                    if yn == 'y':
                        continue9 = 1
                        break
                    elif yn == 'n':
                        continue9 = 0
                        break
                    else:
                        print("Error: Please enter valid input.\n")

        elif command.lower() == '4':
            exit()
        else:
            print("Error: option unavailable, check again:\n")

    # remember to close connection
    cursor.close()
    cnx.close()