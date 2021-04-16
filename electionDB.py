import mysql.connector
from mysql.connector import errorcode
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn import datasets
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable


class electionDB:

    def __init__(self, cursor, cnx):
        self.cursor = cursor
        self.cnx = cnx

    def executeQuery(self, query):
        cursor = self.cursor
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            if err.errno == 2013:
                print("Lost connection, reconnect")
                return -1
            else:
                print(err)

    def testState(self, state):
        query = ("SELECT * FROM States WHERE name = '%s'" % state)
        result = self.executeQuery(query)
        return result
    
    def testCounty(self, county):
        query = ("SELECT * FROM County WHERE name = '%s'" % county)
        result = self.executeQuery(query)
        return result
    
    def testParty(self, party):
        query = ("SELECT * FROM Party WHERE name = '%s'" % party)
        result = self.executeQuery(query)
        return result

    def getListioCountiesUnderState(self, state):
        query = ("""SELECT c.name as countyName 
                            FROM County c
                            inner join States s on (c.stateid = s.stateid)
                            WHERE s.name = '%s'""" % state)
        result = self.executeQuery(query)
        return result

    def totalVotesByState(self, state):
        filterByStateCond = ""
        if state.lower() != 'a':
            filterByStateCond = "having s.name = '" + state + "'"

        query = ("""SELECT  s.name as state ,
                                  sum(total_votes) as total_votes_2020
                            FROM VotesPerCounty v
                            inner join County c on (v.countyid = c.countyid)
                            inner join States s on (c.stateid = s.stateid)
                            group by s.name 
                            %s
                            order by s.name asc""" % filterByStateCond)
        result = self.executeQuery(query)
        return result

    def totalVotesByCounty(self, state, county):
        filterByCountyCond = ""
        if county.lower() != 'a':
            filterByCountyCond = "and c.name = '" + county + "'"

        query = ("""SELECT  s.name as state, c.name as county ,
                                sum(total_votes) as total_votes_2020
                            FROM VotesPerCounty v
                            inner join County c on (v.countyid = c.countyid)
                            inner join States s on (c.stateid = s.stateid)
                            group by c.name, s.name
                            having s.name = '%s' %s
                             order by c.name asc""" % (state, filterByCountyCond))
        result = self.executeQuery(query)
        return result

    def demographicsByState(self, state):
        if state.lower() == 'alaska':
            return -2
        query = ("""select ss.name as 'States' ,
                            ROUND(sum(pop_per_county),2) as 'population',
                            ROUND((sum(demographicMen)/sum(pop_per_county))*100,2) as 'men',
                            ROUND((sum(demographicWomen)/sum(pop_per_county))*100,2) as 'women',
                            ROUND((sum(demographicWhite)/sum(pop_per_county))*100,2) as 'white',
                            ROUND((sum(demographicBlack)/sum(pop_per_county))*100,2) as 'black',
                            ROUND((sum(demographicHispanic)/sum(pop_per_county))*100,2) as 'hispanic',
                            ROUND((sum(demographicAsian)/sum(pop_per_county))*100,2) as 'asian',
                            ROUND((sum(demographicNative)/sum(pop_per_county))*100,2) as 'native',
                            ROUND(avg(income),2) as 'average_income'
                            from (
                                     SELECT  c.name as county, 
                                             c.countyid as countyid,
                                             TotalPop as pop_per_county,
                                             (cs.Men) as demographicMen,
                                             (cs.Women) as demographicWomen,
                                             (cs.White*TotalPop/100) as demographicWhite,
                                             (cs.Black*TotalPop/100) as demographicBlack,
                                             (cs.Hispanic*TotalPop/100) as demographicHispanic,
                                             (cs.Asian*TotalPop/100) as demographicAsian,
                                             (cs.Native*TotalPop/100) as demographicNative,
                                             Income as income
                                     FROM CountyStats cs
                                     inner join County c on (cs.countyid = c.countyid)
                            ) as Stats

                            inner join County co on (co.countyid = Stats.countyid)
                            inner join States ss on (ss.stateid = co.stateid)
                            group by ss.stateid
                            having ss.name = '%s' and ss.name != 'alaska'
                            order by ss.stateid asc""" % state)
        result = self.executeQuery(query)
        return result

    def demographicsByCounty(self, state, county):
        if state.lower() == 'alaska':
            return -2
        query = ("""select ss.name as 'States', co.name as 'County', 
                            ROUND(sum(pop_per_county),2) as 'population',
                            ROUND((sum(demographicMen)/sum(pop_per_county))*100,2) as 'men',
                            ROUND((sum(demographicWomen)/sum(pop_per_county))*100,2) as 'women',
                            ROUND((sum(demographicWhite)/sum(pop_per_county))*100,2) as 'white',
                            ROUND((sum(demographicBlack)/sum(pop_per_county))*100,2) as 'black',
                            ROUND((sum(demographicHispanic)/sum(pop_per_county))*100,2) as 'hispanic',
                            ROUND((sum(demographicAsian)/sum(pop_per_county))*100,2) as 'asian',
                            ROUND((sum(demographicNative)/sum(pop_per_county))*100,2) as 'native',
                            ROUND(sum(income),2) as 'average_income'
                            from (
                                     SELECT  c.name as county, 
                                             c.countyid as countyid,
                                             TotalPop as pop_per_county,
                                             (cs.Men) as demographicMen,
                                             (cs.Women) as demographicWomen,
                                             (cs.White*TotalPop/100) as demographicWhite,
                                             (cs.Black*TotalPop/100) as demographicBlack,
                                             (cs.Hispanic*TotalPop/100) as demographicHispanic,
                                             (cs.Asian*TotalPop/100) as demographicAsian,
                                             (cs.Native*TotalPop/100) as demographicNative,
                                             Income as income
                                     FROM CountyStats cs
                                     inner join County c on (cs.countyid = c.countyid)
                            ) as Stats

                            inner join County co on (co.countyid = Stats.countyid)
                            inner join States ss on (ss.stateid = co.stateid)
                            group by ss.stateid, co.countyid
                            having ss.name = '%s' and co.name = '%s'  and ss.name != 'alaska'
                            order by ss.stateid asc""" % (state, county))
        result = self.executeQuery(query)
        return result

    def tweetsBiden(self, state, number):
        if not number:
            number = 5

        query = ("""SELECT s.name, created_at, tweet, likes, retweets 
                    FROM TweetsBiden t
                    inner join States s on (t.stateid = s.stateid)
                    WHERE s.name = '%s'
                    ORDER BY t.likes DESC
                    limit %s""" % (state, number))
        result = self.executeQuery(query)
        return result

    def tweetsTrump(self, state, number):
        if not number:
            number = 5

        query = ("""SELECT s.name, created_at, tweet, likes, retweets 
                    FROM TweetsTrump t
                    inner join States s on (t.stateid = s.stateid)
                    WHERE s.name = '%s'
                    ORDER BY t.likes DESC
                    limit %s""" % (state, number))
        result = self.executeQuery(query)
        return result

    def votingResultsbyPartybyState(self, state, winnerForState=0, limiter=0):
        filterByStateCond = winner = limit = ""
        if winnerForState == 1:
            winner = "where won = 'True'"
        if limiter == 1:
            limit = " limit 1"
        if state.lower() != 'a':
            filterByStateCond = "having s.name = '" + state + "'"

        query = ("""SELECT  s.name as state, 
                            p.name as party,
                            sum(total_votes) as total_votes_2020
                            FROM VotesPerCounty v

                            inner join County c on (v.countyid = c.countyid)
                            inner join States s on (c.stateid = s.stateid)
                            inner join Party p on (p.partyid = v.partyid)
                            %s
                            group by v.partyid, s.stateid
                            %s
                            order by s.stateid asc %s""" % (winner, filterByStateCond, limit))
        result = self.executeQuery(query)
        return result




    def getResultsForAllStates(self):

        query = ("""with topVoted as (SELECT  s.name as state, s.stateid,
                            p.name as party,
                            sum(total_votes) as total_votes_2020
                            FROM VotesPerCounty v

                            inner join County c on (v.countyid = c.countyid)
                            inner join States s on (c.stateid = s.stateid)
                            inner join Party p on (p.partyid = v.partyid)
                            where won = 'True'
                            group by v.partyid, s.stateid
                            order by s.stateid, sum(total_votes))
                select state, party, total_votes_2020 from topVoted 
                where total_votes_2020 in
                        (
                        select max(total_votes_2020) 
                        from topVoted
                        inner join States s on (s.stateid = topVoted.stateid)
                        group by  s.stateid)""")
        result = self.executeQuery(query)
        return result

    def votingResultsbyPartybyCounty(self, state, county, results):
        winning = ""
        filterByStateCond = ""
        if results == 1:
            winning = " and v.won = 'True'"
        if county.lower() != 'a':
            filterByStateCond = "and c.name = '" + county + "'"

        query = ("""SELECT  s.name as state, 
                   c.name as county, 
                   p.name as party ,
                   total_votes as total_votes_2020
                  FROM VotesPerCounty v
                
                  inner join County c on (v.countyid = c.countyid)
                  inner join States s on (c.stateid = s.stateid)
                  inner join Party p on (p.partyid = v.partyid)
                
                  where s.name = '%s' %s %s
                  order by c.countyid asc""" % (state, filterByStateCond, winning))
        result = self.executeQuery(query)
        return result

    def addResults(self, state, county, party, result):
        cnx = self.cnx

        countyid = 0
        # get stateid and countyid
        if county != 0:
            query = ("""select s.stateid, c.countyid from County c
                        inner join States s on (s.stateid = c.stateid)
                        where s.name = '%s' 
                        and c.name = '%s'""" % (state, county))
            result1 = self.executeQuery(query)
            if (result1 == -1):
                return -1
            for i in result1:
                stateid = i[0]
                countyid = i[1]
        else:
            query = ("""select s.stateid from States s where s.name = '%s'""" % (state))
            result1 = self.executeQuery(query)
            if (result1 == -1):
                return -1
            for i in result1:
                stateid = i[0]

        # get partyid
        query = ("""select partyid from Party where name = '%s'""" % party)
        result2 = self.executeQuery(query)
        if (result2 == -1):
            return -1
        for i in result2:
            partyid = i[0]

        # QUERY
        if countyid == 0:
            query = ("""INSERT INTO electionComments (stateid, countyid, partyid, result) 
                    VALUES (%d, NULL, %d, '%s')""" % (stateid, partyid, result))
        else:
            query = ("""INSERT INTO electionComments (stateid, countyid, partyid, result) 
                    VALUES (%d, %d, %d, '%s')""" % (stateid, countyid, partyid, result))
        result = self.executeQuery(query)
        if (result == -1):
            return -1

        cnx.commit()

        return 0

    # DATA MINING STUFF - results and demographics for a county
    def getData(self):

        query = ("""select 
                    ROUND(sum(pop_per_county),2) as 'population',
                    ROUND((sum(demographicMen)/sum(pop_per_county))*100,2) as 'men',
                    ROUND((sum(demographicWomen)/sum(pop_per_county))*100,2) as 'women',
                    ROUND((sum(demographicWhite)/sum(pop_per_county))*100,2) as 'white',
                    ROUND((sum(demographicBlack)/sum(pop_per_county))*100,2) as 'black',
                    ROUND((sum(demographicHispanic)/sum(pop_per_county))*100,2) as 'hispanic',
                    ROUND((sum(demographicAsian)/sum(pop_per_county))*100,2) as 'asian',
                    ROUND((sum(demographicNative)/sum(pop_per_county))*100,2) as 'native',
                    ROUND(sum(income),2) as 'average_income',
                    ROUND((sum(demographicPoverty)/sum(pop_per_county))*100,2) as 'poverty',
                    ROUND((sum(demographicEmployed)/sum(pop_per_county))*100,2) as 'employed',
                    ROUND((sum(demographicUnemployment)/sum(pop_per_county))*100,2) as 'unemployed',
                    p.partyid as 'winning_party'
                    from (
                             SELECT  c.name as county, 
                                     c.countyid as countyid,
                                     TotalPop as pop_per_county,
                                     (cs.Men) as demographicMen,
                                     (cs.Women) as demographicWomen,
                                     (cs.White*TotalPop/100) as demographicWhite,
                                     (cs.Black*TotalPop/100) as demographicBlack,
                                     (cs.Hispanic*TotalPop/100) as demographicHispanic,
                                     (cs.Asian*TotalPop/100) as demographicAsian,
                                     (cs.Native*TotalPop/100) as demographicNative,
                                     Income as income,
                                     (cs.Poverty*TotalPop/100) as demographicPoverty,
                                     Employed as demographicEmployed,
                                     (cs.Unemployment*TotalPop/100) as demographicUnemployment
                             FROM CountyStats cs
                             inner join County c on (cs.countyid = c.countyid)
                    ) as Stats
                    
                    inner join County co on (co.countyid = Stats.countyid)
                    inner join States ss on (ss.stateid = co.stateid)
                    inner join VotesPerCounty vpc on (vpc.countyid = Stats.countyid)
                    inner join Party p on (vpc.partyid = p.partyid)
                    
                    group by ss.stateid, co.countyid, vpc.won, p.partyid 
                    having vpc.won  = 'True' and p.partyid = 1 or p.partyid = 2
                    order by ss.stateid asc""")
        data = self.executeQuery(query)

        success = self.generateCSV(data)
        return success

    def generateCSV(self, data):

        cursor = self.cursor
        column_names = [i[0] for i in cursor.description]
        fp = open('demographics_and_votes.csv', 'w', encoding="utf-8")
        myFile = csv.writer(fp, lineterminator='\n')
        myFile.writerow(column_names)
        myFile.writerows(data)
        fp.close()

        return 0

    def computeData(self):

        # define our labels
        labels = ["Democratic", "Republican"]
        features = ["population", "men", "women", "white", "black", "hispanic", "asian", "native",
                    "average_income", "poverty", "employed", "unemployed"]

        # load data into numpy array
        mydata = np.genfromtxt("demographics_and_votes.csv", dtype=None, delimiter=',', names=True)

        # create dataframe
        data = pd.DataFrame({
            'population': mydata["population"],
            'men': mydata["men"],
            'women': mydata["women"],
            'white': mydata["white"],
            'black': mydata["black"],
            'hispanic': mydata["hispanic"],
            'asian': mydata["asian"],
            'native': mydata["native"],
            'average_income': mydata["average_income"],
            'poverty': mydata["poverty"],
            'employed': mydata["employed"],
            'unemployed': mydata["unemployed"],
            'winning_party': mydata["winning_party"]
        })
        # print(data.head())

        X = data[['population', 'men', 'women', 'white', 'black', 'hispanic', 'asian', 'native',
                  'average_income', 'poverty', 'employed', 'unemployed']]  # Features
        y = data['winning_party']  # Labels

        # Split dataset into training set and test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)  # 70% training and 30% test
        X_train.fillna(X_train.mean(), inplace=True)
        X_test.fillna(X_test.mean(), inplace=True)

        # Create a Gaussian Classifier
        clf = RandomForestClassifier(n_estimators=200)

        # Train the model using the training sets
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        prediction = str(round(metrics.accuracy_score(y_test, y_pred)*100, 3))+"%"
        # print("....................................................................")
        # print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
        # print("....................................................................")


        # plot
        feature_imp = pd.Series(clf.feature_importances_, index=features).sort_values(ascending=False)
        table = PrettyTable(['Demographic', 'Percentage Influence'])
        for index, val in feature_imp.iteritems():
            table.add_row([index, str(round(val*100, 3))+"%"])

        # # Creating a bar plot
        # sns.barplot(x=feature_imp, y=feature_imp.index)
        #
        # # Add labels to your graph
        # plt.xlabel('Feature Importance Score')
        # plt.ylabel('Features')
        # plt.title("Visualizing Important Features")
        # plt.legend()
        # plt.show()

        return prediction, table

    def predictData(self):
        return 0
