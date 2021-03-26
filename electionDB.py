import mysql.connector
from mysql.connector import errorcode
import locale
import decimal
import fire
import getpass
import sys


class electionDB:

    def __init__(self, cursor):
        self.cursor = cursor


    def getListioCountiesUnderState(self, state):

        cursor = self.cursor

        query = ("""SELECT name as countyName FROM County WHERE state = '%s'""" % state)
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def totalVotesByState(self, state):

        cursor = self.cursor
        filterByStateCond = ""
        if (state != 'a' and state != 'A'):
            filterByStateCond = "having c.state = '" + state + "'"

        query = ("""SELECT  c.state as state ,
                          sum(total_votes) as total_votes_2020
                  FROM VotesPerCounty v
                  inner join County c on (v.county = c.name)
                  group by c.state
                  %s
                  order by c.state asc""" % filterByStateCond)
        cursor.execute(query)
        result = cursor.fetchall()
        return result



    def totalVotesByCounty(self, county):

        cursor = self.cursor
        query = ("""SELECT  c.name as county ,
                          sum(total_votes) as total_votes_2020
                  FROM VotesPerCounty v
                  inner join County c on (v.county = c.name)
                  group by c.name
                  having c.name = '%s'
                  order by c.name asc""" % county)
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def demographicsByState(self, state):

        cursor = self.cursor
        filterByStateCond = ""
        if (state != 'a' and state != 'A'):
            filterByStateCond = "cs.state = '" + state + "' and"

        query = ("""select cs.state as 'States', 
                         ROUND(sum(pop_per_county),2) as 'Total Population',
                         ROUND((sum(demographicMen)/sum(pop_per_county))*100,2) as 'Percentage of Men',
                         ROUND((sum(demographicWomen)/sum(pop_per_county))*100,2) as 'Percentage of Women',
                         ROUND((sum(demographicWhite)/sum(pop_per_county))*100,2) as 'Percentage of White',
                         ROUND((sum(demographicBlack)/sum(pop_per_county))*100,2) as 'Percentage of Black',
                         ROUND((sum(demographicHispanic)/sum(pop_per_county))*100,2) as 'Percentage of Hispanic',
                         ROUND((sum(demographicAsian)/sum(pop_per_county))*100,2) as 'Percentage of Asian',
                         ROUND((sum(demographicNative)/sum(pop_per_county))*100,2) as 'Percentage of Native',
                         ROUND((sum(demographicPacific)/sum(pop_per_county))*100,2) as 'Percentage of Pacific'
                     from (
                         SELECT  c.name as county, 
                         TotalPop as pop_per_county,

                         (s.Men) as demographicMen,
                         (s.Women) as demographicWomen,
                         (s.White*TotalPop/100) as demographicWhite,
                         (s.Black*TotalPop/100) as demographicBlack,
                         (s.Hispanic*TotalPop/100) as demographicHispanic,
                         (s.Asian*TotalPop/100) as demographicAsian,
                         (s.Native*TotalPop/100) as demographicNative,
                         (s.Pacific*TotalPop/100) as demographicPacific

                         FROM CountyStats s
                         inner join County c on (s.countyid = c.countyid)
                     ) as Stats

                     inner join County cs on (cs.name = county)
                     group by cs.state
                     having %s cs.state != 'Alaska'
                     order by cs.state asc""" % filterByStateCond)
        cursor.execute(query)
        result = cursor.fetchall()
        return result
