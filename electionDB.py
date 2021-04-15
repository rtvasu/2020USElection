import mysql.connector
from mysql.connector import errorcode
import locale
import decimal
import fire
import getpass
import sys
import csv


class electionDB:

    def __init__(self, cursor, cnx):
        self.cursor = cursor
        self.cnx = cnx

    def getListioCountiesUnderState(self, state):

        cursor = self.cursor

        query = ("""SELECT c.name as countyName 
                    FROM County c
                    inner join States s on (c.stateid = s.stateid)
                    WHERE s.name = '%s'""" % state)
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def totalVotesByState(self, state):

        cursor = self.cursor
        filterByStateCond = ""
        if state.lower != 'a':
            filterByStateCond = "having s.name = '" + state + "'"

        query = ("""SELECT  s.name as state ,
                          sum(total_votes) as total_votes_2020
                    FROM VotesPerCounty v
                    inner join County c on (v.countyid = c.countyid)
                    inner join States s on (c.stateid = s.stateid)
                    group by s.name 
                    %s
                    order by s.name asc""" % filterByStateCond)
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def totalVotesByCounty(self, state, county):

        cursor = self.cursor
        filterByCountyCond = ""
        if county.lower != 'a':
            filterByCountyCond = "and c.name = '" + county + "'"

        query = ("""SELECT  s.name as state, c.name as county ,
                        sum(total_votes) as total_votes_2020
                    FROM VotesPerCounty v
                    inner join County c on (v.countyid = c.countyid)
                    inner join States s on (c.stateid = s.stateid)
                    group by c.name, s.name
                    having s.name = '%s' %s
                     order by c.name asc""" % (state, filterByCountyCond))
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def demographicsByState(self, state):

        cursor = self.cursor
        # if (state != 'a' and state != 'A'):
        filterByStateCond = "ss.name = '" + state + "'"

        query = ("""select ss.name as 'States', 
                         ROUND(sum(pop_per_county),2) as 'Total Population',
                         ROUND((sum(demographicMen)/sum(pop_per_county))*100,2) as 'Percentage of Men',
                         ROUND((sum(demographicWomen)/sum(pop_per_county))*100,2) as 'Percentage of Women',
                         ROUND((sum(demographicWhite)/sum(pop_per_county))*100,2) as 'Percentage of White',
                         ROUND((sum(demographicBlack)/sum(pop_per_county))*100,2) as 'Percentage of Black',
                         ROUND((sum(demographicHispanic)/sum(pop_per_county))*100,2) as 'Percentage of Hispanic',
                         ROUND((sum(demographicAsian)/sum(pop_per_county))*100,2) as 'Percentage of Asian',
                         ROUND((sum(demographicNative)/sum(pop_per_county))*100,2) as 'Percentage of Native'
                     from (
                         SELECT  c.name as county, 
                         TotalPop as pop_per_county,

                         (cs.Men) as demographicMen,
                         (cs.Women) as demographicWomen,
                         (cs.White*TotalPop/100) as demographicWhite,
                         (cs.Black*TotalPop/100) as demographicBlack,
                         (cs.Hispanic*TotalPop/100) as demographicHispanic,
                         (cs.Asian*TotalPop/100) as demographicAsian,
                         (cs.Native*TotalPop/100) as demographicNative

                         FROM CountyStats cs
                         inner join County c on (cs.countyid = c.countyid)
                         inner join States s on (c.stateid = s.stateid)
                     ) as Stats

                     inner join County co on (co.name = county)
                     inner join States ss on (co.stateid = ss.stateid)
                     group by ss.name 
                     having %s
                     order by ss.name asc""" % filterByStateCond)
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def demographicsByCounty(self, state, county):

        cursor = self.cursor
        # if (state != 'a' and state != 'A'):
        filterByCountyCond = "and c.name = '" + county + "'"

        query = ("""select ss.name as 'States', co.name as 'County', 
                         ROUND(sum(pop_per_county),2) as 'Total Population',
                         ROUND((sum(demographicMen)/sum(pop_per_county))*100,2) as 'Percentage of Men',
                         ROUND((sum(demographicWomen)/sum(pop_per_county))*100,2) as 'Percentage of Women',
                         ROUND((sum(demographicWhite)/sum(pop_per_county))*100,2) as 'Percentage of White',
                         ROUND((sum(demographicBlack)/sum(pop_per_county))*100,2) as 'Percentage of Black',
                         ROUND((sum(demographicHispanic)/sum(pop_per_county))*100,2) as 'Percentage of Hispanic',
                         ROUND((sum(demographicAsian)/sum(pop_per_county))*100,2) as 'Percentage of Asian',
                         ROUND((sum(demographicNative)/sum(pop_per_county))*100,2) as 'Percentage of Native'
                     from (
                         SELECT  c.name as county, 
                         TotalPop as pop_per_county,

                         (cs.Men) as demographicMen,
                         (cs.Women) as demographicWomen,
                         (cs.White*TotalPop/100) as demographicWhite,
                         (cs.Black*TotalPop/100) as demographicBlack,
                         (cs.Hispanic*TotalPop/100) as demographicHispanic,
                         (cs.Asian*TotalPop/100) as demographicAsian,
                         (cs.Native*TotalPop/100) as demographicNative

                         FROM CountyStats cs
                         inner join County c on (cs.countyid = c.countyid)
                         inner join States s on (c.stateid = s.stateid)
                     ) as Stats

                     inner join County co on (co.name = county)
                     inner join States ss on (co.stateid = ss.stateid)
                     group by ss.name, co.name
                     having ss.name = '%s' and co.name = '%s'
                     order by ss.name asc""" % (state, county))
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def tweetsBiden(self, state, number):

        cursor = self.cursor

        if (not number):
            number = 5

        query = ("""SELECT s.name, created_at, tweet, likes, retweets 
                    FROM TweetsBiden t
                    inner join States s on (t.stateid = s.stateid)
                    WHERE s.name = '%s'
                    ORDER BY t.likes DESC
                    limit %s""" % (state, number))
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def tweetsTrump(self, state, number):

        cursor = self.cursor

        if (not number):
            number = 5

        query = ("""SELECT s.name, created_at, tweet, likes, retweets 
                    FROM TweetsTrump t
                    inner join States s on (t.stateid = s.stateid)
                    WHERE s.name = '%s'
                    ORDER BY t.likes DESC
                    limit %s""" % (state, number))
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def votingResultsbyPartybyState(self, state, results=0):

        cursor = self.cursor
        limit = ""
        if results == 1:
            limit = " limit 1"

        query = ("""SELECT  s.name as state, p.name as party ,
                   sum(total_votes) as total_votes_2020
               FROM VotesPerCounty v
               inner join County c on (v.countyid = c.countyid)
               inner join States s on (c.stateid = s.stateid)
               inner join Party p on (p.partyid = v.partyid)
               group by s.name, p.name 
               having s.name = '%s'
                order by sum(total_votes) desc %s""" % (state, limit))
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def votingResultsbyPartybyCounty(self, state, county, results):

        cursor = self.cursor
        limit = ""
        if results == 1:
            limit = " limit 1"

        query = ("""SELECT  s.name as state, c.name as county, p.name as party ,
               sum(total_votes) as total_votes_2020
           FROM VotesPerCounty v
           inner join County c on (v.countyid = c.countyid)
           inner join States s on (c.stateid = s.stateid)
            inner join Party p on (p.partyid = v.partyid)
           group by s.name, c.name, p.name 
           having s.name = '%s' and c.name = '%s'
            order by sum(total_votes) desc %s""" % (state, county, limit))
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def addResults(self, state, county, party, result):
        cursor = self.cursor
        cnx = self.cnx

        countyid = 0
        # get stateid and countyid
        if (county != 0):
            query = ("""select s.stateid, c.countyid from County c
                        inner join States s on (s.stateid = c.stateid)
                        where s.name = '%s' 
                        and c.name = '%s'""" % (state, county))
            cursor.execute(query)
            result1 = cursor.fetchall()
            for i in result1:
                stateid = i[0]
                countyid = i[1]
        else:
            query = ("""select s.stateid from States s where s.name = '%s'""" % (state))
            cursor.execute(query)
            result1 = cursor.fetchall()
            for i in result1:
                stateid = i[0]

        # get partyid
        query = ("""select partyid from Party where abbreviation = '%s'""" % party)
        cursor.execute(query)
        result2 = cursor.fetchall()
        for i in result2:
            partyid = i[0]

        # QUERY
        if countyid == 0:
            query = ("""INSERT INTO winAndLosses (stateid, countyid, partyid, result) 
                    VALUES (%d, NULL, %d, '%s')""" % (stateid, partyid, result))
        else:
            query = ("""INSERT INTO winAndLosses (stateid, countyid, partyid, result) 
                    VALUES (%d, %d, %d, '%s')""" % (stateid, countyid, partyid, result))
        cursor.execute(query)

        cnx.commit()

        return 0

    # DATA MINING STUFF - results and demographics for a county
    def getData(self, state, county):
        cursor = self.cursor

        query = ("""select ss.name as 'States', 
                    co.name as 'County', 
                    p.abbreviation as 'winningParty' ,
                    ROUND(sum(pop_per_county),2) as 'Total Population',
                    ROUND((sum(demographicMen)/sum(pop_per_county))*100,2) as 'Percentage of Men',
                    ROUND((sum(demographicWomen)/sum(pop_per_county))*100,2) as 'Percentage of Women',
                    ROUND((sum(demographicWhite)/sum(pop_per_county))*100,2) as 'Percentage of White',
                    ROUND((sum(demographicBlack)/sum(pop_per_county))*100,2) as 'Percentage of Black',
                    ROUND((sum(demographicHispanic)/sum(pop_per_county))*100,2) as 'Percentage of Hispanic',
                    ROUND((sum(demographicAsian)/sum(pop_per_county))*100,2) as 'Percentage of Asian',
                    ROUND((sum(demographicNative)/sum(pop_per_county))*100,2) as 'Percentage of Native',
                    ROUND(sum(income),2) as 'Average Income',
                    ROUND((sum(demographicPoverty)/sum(pop_per_county))*100,2) as 'Percentage living under poverty',
                    ROUND((sum(demographicEmployed)/sum(pop_per_county))*100,2) as 'Percentage employed',
                    ROUND((sum(demographicUnemployment)/sum(pop_per_county))*100,2) as 'Percentage unemployed'
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
                    having ss.name = '%s' and co.name = '%s' and vpc.won  = 'True'
                    order by ss.name asc""" % (state, county))
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def generateCSV(self, data):

        cursor = self.cursor

        column_names = [i[0] for i in cursor.description]
        fp = open('demographics_and_votes.csv', 'w')
        myFile = csv.writer(fp, lineterminator='\n')
        myFile.writerow(column_names)
        myFile.writerows(data)
        fp.close()

        return 0

    def computerData(self):
        return 0

    def predictData(self):
        return 0
