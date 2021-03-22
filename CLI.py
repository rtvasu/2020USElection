import mysql.connector
from mysql.connector import errorcode

config = {
    'user':'usr',#insert your user name here
    'password':'pwd',#insert your password here
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
#else, execute query
else:
    cursor = cnx.cursor()
    query = ("SELECT MAX(deaths) AS maxDeaths from CountyStats;")
    cursor.execute(query)
    for (maxDeaths) in cursor:
        print("{}".format(maxDeaths))
    
    #remember to close connection
    cursor.close()
    cnx.close()