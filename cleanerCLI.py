import mysql.connector
from mysql.connector import errorcode
import getpass
from electionDB import electionDB
import locale
import numbers

def startup():
    # get username and password
    print("..........................................................................................")
    username = input("Username: ")
    password = getpass.getpass(prompt='Password: ', stream=None)

    config = {
        'user': username,
        'password': password,
        'host': 'marmoset04.shoshin.uwaterloo.ca',
        'database': 'project_1',
        'raise_on_warnings': True
    }

    locale.setlocale(locale.LC_ALL, 'en_US')

    # attempt to establish connection
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Something is wrong with your user name or password, try again.")
            return (-1, -1)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist")
            exit()
        else:
            print(err)
            return (-1, -1)
    return cnx, cursor

def homepage(results):
    print("..........................................................................................")
    print(".................................. HOME PAGE ......................................")
    print("..........................................................................................\n")

    print("Please select an option and enter the number:")
    print("[1] Get statistics")
    print("[2] Insert Data")
    print("[3] Data Mine")
    print("[4] Exit")
    print("\n")

    validCommand = 0
    while validCommand == 0:
        command = input("Your command: ")
        try:
            if (int(command.lower()) < 1) or (int(command.lower()) > 4):
                print("Please enter a valid option.")
                continue
            else:
                validCommand = 1
        except:
            print("Please enter a valid option.")
            continue
    
    if (int(command.lower()) == 4):
        exit()
    menu = {
        1: getStats,
        2: insertData,
        3: dataMine,
        4: exit
    }

    continueExecution = 1
    #shorthand to call respective function
    where = menu[int(command.lower())](results)
    print(where)

    while continueExecution == 1:
        #user wants to see getStats/insertData/dataMine again
        if where == 0:
            where = menu[int(command.lower())](results)
        #user wants to see home page
        elif where == 1:
            return 1

def getCorrectState(results):
    correctState = 0
    while correctState == 0:
        stateInput = input("Please enter name of state: ")
        if not stateInput:
            print("\nError: Please enter a value.\n")
            continue
        test = results.testState(stateInput)
        if (not test):
            print("\nError: Check if state exists and is spelled correctly.\n")
        else:
            correctState = 1
    return stateInput

def getCorrectCounty(results):
    correctCounty = 0
    while correctCounty == 0:
        countyInput = input("Here is a list of counties in this state. Please choose a county to view results for: ")
        if not countyInput:
            print("\nError: Please enter a value.\n")
            continue
        test = results.testCounty(countyInput)
        if (not test):
            print("\nError: Check if county exists and is spelled correctly.\n")
        else:
            correctCounty = 1
    return countyInput

def getCorrectParty(results):
    correctParty = 0
    while correctParty == 0:
        partyInput = input("State party from above list: ")
        if not partyInput:
            print("\nError: Please enter a value.\n")
            continue
        test = results.testParty(partyInput)
        if (not test):
            print("\nError: Check if party exists (cannot be None) and is spelled correctly.\n")
        else:
            correctParty = 1
    return partyInput

def votingResultsForState(results):
    print("..........................................................................................")
    print("............................... VOTING RESULTS FOR A STATE ...............................")
    print("..........................................................................................")
    print("\n")

    # get correct state
    stateInput = getCorrectState(results)
    
    # get total number of votes
    totalVotes = results.totalVotesByState(stateInput)

    # this is a reaaally edge case
    if not totalVotes:
        print("Unknown error")
        exit()
    # this is likely, happens when connection is lost
    if (totalVotes == -1):
        exit()
    
    totalResults = results.votingResultsbyPartybyState(stateInput, 1, 1)
    # this is a reaaally edge case
    if not totalResults:
        print("Unknown error")
        exit()
    elif totalResults == -1:
        exit()
    
    #TODO: help aish, fix totalVotes (or double check if what I've done is correct)
    for i in totalVotes:
        state = locale.format_string("%s", i[0], grouping=True)
        votes_total = locale.format_string("%d", i[1], grouping=True)

    for i in range(len(totalResults)):
        party = locale.format_string("%s", totalResults[i][1], grouping=True)
        votes = locale.format_string("%d", totalResults[i][2], grouping=True)
        # votes_total = locale.format_string("%d", totalVotes[i][1], grouping=True)
        print("The winning party in ", state, " is ", party,
                " with " + votes + " votes & the total votes =  ", votes_total)
    print("\n")

def votingResultsForAllStates(results):
    print("..........................................................................................")
    print("............................. VOTING RESULTS FOR ALL STATES ..............................")
    print("..........................................................................................")
    print("\n")
    totalVotes = results.totalVotesByState('a')
    totalResults = results.getResultsForAllStates()
    if not totalVotes:
        exit()
    elif(totalVotes == -1 or totalResults == -1):
        exit()

    # for i in totalVotes:
    #     votes_total = locale.format_string("%d", i[1], grouping=True)

    #TODO: help aish, fix totalVotes (or double check if what I've done is correct)
    for i in range(len(totalResults)):
        state = locale.format_string("%s", totalResults[i][0], grouping=True)
        party = locale.format_string("%s", totalResults[i][1], grouping=True)
        votes = locale.format_string("%d", totalResults[i][2], grouping=True)
        votes_total = locale.format_string("%d", totalVotes[i][1], grouping=True)
        print("The winning party in ", state, " is ", party,
                " with " + votes + " votes & the total votes =  ", votes_total)
    print("\n")

def votingResultsForCounty(results):
    print("..........................................................................................")
    print(".........................,.... VOTING RESULTS FOR A COUNTY ...............................")
    print("..........................................................................................")
    print("\n")

    stateInput = getCorrectState(results)

    countyList = results.getListioCountiesUnderState(stateInput)
    if not countyList:
        print("Error: Check if state exists and is spelled correctly.\n")
    elif(countyList == -1):
        exit()
    else:
        for i in countyList:
            print(i[0])
        print("\n")

        county = getCorrectCounty(results)

        countyTotalResults = results.totalVotesByCounty(stateInput, county)
        countyVotingResults = results.votingResultsbyPartybyCounty(stateInput, county, 1)

        if (not countyTotalResults) or (not countyVotingResults):
            exit()
        elif countyTotalResults == -1 or countyVotingResults == -1:
            exit()
        
        for i in countyTotalResults:
            total_votes = locale.format_string("%d", i[2], grouping=True)

        for i in countyVotingResults:
            county = locale.format_string("%s", i[1], grouping=True)
            party = locale.format_string("%s", i[2], grouping=True)
            votes = locale.format_string("%d", i[3], grouping=True)
            print("The winning party in ", county, " is ", party,
                    " with " + votes + " votes & the total votes =  ", total_votes)
        print("\n")

def votingResultsForAllCounties(results):
    print("..........................................................................................")
    print("...................... VOTING RESULTS FOR ALL COUNTIES IN A STATE ........................")
    print("..........................................................................................")
    print("\n")

    stateInput = getCorrectState(results)

    countyList = results.getListioCountiesUnderState(stateInput)
    if not countyList:
        print("Error: Check if state exists and is spelled correctly.\n")
    elif(countyList == -1):
        exit()
    else:
        countyTotalVotes = results.totalVotesByCounty(stateInput, 'A')
        countyVotingResults = results.votingResultsbyPartybyCounty(stateInput, 'A', 1)

        if not countyTotalVotes:
            print("Error: Check if county exists and is spelled correctly.\n")
        elif countyTotalVotes == -1 or countyVotingResults == -1:
            exit()
        else:
            #TODO: correct total_votes aish
            for i in countyTotalVotes:
                total_votes = locale.format_string("%d", i[2], grouping=True)

            for i in countyVotingResults:
                county = locale.format_string("%s", i[1], grouping=True)
                party = locale.format_string("%s", i[2], grouping=True)
                votes = locale.format_string("%d", i[3], grouping=True)
                print("The winning party in ", county, " is ", party,
                        " with " + votes + " votes & the total votes =  ", total_votes)
            print("\n")

def getCorrectNumTweets(results):
    correctNum = 0
    while correctNum == 0:
        numberOfTweets = input("How many tweets do you want to view? ")
        print("\n")
        if not numberOfTweets:
            print("Please enter an input.\n")
            continue
        try:
            if (int(numberOfTweets) < 1):
                print("Please enter a valid number of tweets.")
                continue
        except:
            print("Please enter a valid number of tweets.")
            continue
        else:
            correctNum = 1
    return numberOfTweets

def mostPopularTweets(results):
    print("..........................................................................................")
    print(".............................. MOST POPULAR TWEETS IN STATE ..............................")
    print("..........................................................................................")
    print("\n")

    stateInput = getCorrectState(results)

    numberOfTweets = getCorrectNumTweets(results)

    bidenTweets = results.tweetsBiden(stateInput, numberOfTweets)
    if not bidenTweets:
        exit()
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
        print("Error: Check if state exists, is spelled correctly and if number is valid.\n")
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

def demoState(results):
    print("..........................................................................................")
    print("................................. DEMOGRAPHICS OF A STATE ................................")
    print("..........................................................................................")
    print("\n")

    state = getCorrectState(results)

    demographics = results.demographicsByState(state)

    if not demographics:
        print("Error: Check if state exists and is spelled correctly.\n")
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

def demoCounty(results):
    print("..........................................................................................")
    print("................................. DEMOGRAPHICS OF A COUNTY ................................")
    print("..........................................................................................")
    print("\n")

    stateInput = getCorrectState(results)

    countyList = results.getListioCountiesUnderState(stateInput)
    if not countyList:
        exit()
    elif(countyList == -1):
        exit()
    else:
        for i in countyList:
            print(i[0])
        print("\n")

        county = getCorrectCounty(results)
        demographics = results.demographicsByCounty(stateInput, county)

        if not demographics:
            print("Error: Check if county exists and is spelled correctly.\n")
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

def checkContinue():
    while 1:
        yn = input("Continue? Y/N: ").lower()
        if yn == 'y':
            return 1
        elif yn == 'n':
            return 0
        else:
            print("Error: Please enter valid input.\n")

# returns 0 when user wants to see getStats menu, 1 when user wants to see home page menu
def getStats(results):
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

    validCommand = 0
    while validCommand == 0:
        command = input("Your command: ")
        try:
            if (int(command.lower()) < 1) or (int(command.lower()) > 7):
                return 1
            else:
                validCommand = 1
        except:
            return 1
    menu = {
        1: votingResultsForState,
        2: votingResultsForAllStates,
        3: votingResultsForCounty,
        4: votingResultsForAllCounties,
        5: mostPopularTweets,
        6: demoState,
        7: demoCounty
    }

    continueExecution = 1
    while continueExecution == 1:
        #shorthand to call respective function
        menu[int(command.lower())](results)
        continueExecution = checkContinue()

    return continueExecution

# returns 0 when user wants to start over the insertData process
def insertData(results):
    print("..........................................................................................")
    print(".................................. ADD YOUR COMMENT ......................................")
    print("..........................................................................................")
    print("\n")

    print("..........................................................................................")
    print("You can add any comment for a state or county")
    print("\n")

    state = getCorrectState(results)
    while 1:
        yn = input("Do you want to select a county? Y/N: ").lower()
        if (yn == 'y') or (yn == 'n'):
            break
        else:
            print("Error: Please enter valid input.\n")
    print("\n")

    # Getting the county
    if yn.lower() == 'y':

        # List of counties
        countyList = results.getListioCountiesUnderState(state)
        if not countyList:
            print("Unknown error :(")
            exit()
        elif countyList == -1:
            exit()
        else:
            for i in countyList:
                print("- " + i[0])
        print("\n")

        county = getCorrectCounty(results)
        print("\n")

        # Get the winning and losing votes
        print("..........................................................................................")
        print(".................................. CURRENT RESULTS .......................................")
        print("..........................................................................................")
        countyResults = results.votingResultsbyPartybyCounty(state, county, 0)

        if not countyResults:
            print("Sorry, no results available for this county. Check if county exists and is spelled correctly.\n")
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
            party = getCorrectParty(results)
            result = input("Enter comment for county: ")
            success = results.addResults(state, county, party, result)
            print("\n")

            if success == 0:
                print("Successfully added comment!")
                return not(checkContinue())
            elif success == -1:
                exit()
            else:
                print("Sorry, try again")
                return 0
            print("\n")


    elif yn.lower() == 'n':
        # Get the winning and losing votes
        print("..........................................................................................")
        print(".................................. CURRENT RESULTS .......................................")
        print("..........................................................................................")

        stateResults = results.votingResultsbyPartybyState(state, 0)

        if not stateResults:
            print("Sorry, no results available for this state. Check if state exists and is spelled correctly.\n")
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
        party = getCorrectParty(results)
        result = input("Enter comment for state: ")
        success = results.addResults(state, 0, party, result)

        if success == 0:
            print("Successfully added comment!")
            return not(checkContinue())
        elif success == -1:
            exit()
        else:
            print("Sorry, try again.\n")
            return 0

def dataMine(results):
    print("..........................................................................................")
    print(".................................. DATA MINING ......................................")
    print("..........................................................................................")

    print("\n")
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
    return 1

def root():

    print("..........................................................................................")
    print("..........................................................................................")
    print("......................... WELCOME TO 2020 ELECTION DATABASE ..............................")
    print("..........................................................................................")
    print("..........................................................................................")
    print("\n")

    # keep trying till success on connection
    successConnect = 0
    while successConnect == 0:
        cnx, cursor = startup()
        if (cnx == -1 and cursor == -1):
            continue
        else:
            successConnect = 1
    
    # initialize electionDB class object
    results = electionDB(cursor, cnx)

    #shorthand to call respective function
    where = homepage(results)

    # where exists only when user has gone inside and wants to see home page again
    if where:

        #this is okay because if home page ever returns, it's because it wants to see the home page again
        while 1:
            #user wants to see homepage again
            homepage(results)

    cursor.close()
    cnx.close()
    return

root()
exit()