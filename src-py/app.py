##
## Author: Victor Nguyen 
## Date: Oct 2023
## Connect to MySQL DB from Python Flask app running wihin a docker conntained 
## Run:
## docker-compose up --build
## 

import time

import yaml 
import mysql.connector
import logging 
from sys import stdout

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


# Define logger
logger = logging.getLogger('mylogger')

logger.setLevel(logging.DEBUG) # set logger level
logFormatter = logging.Formatter("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
consoleHandler = logging.StreamHandler(stdout) #set streamhandler to stdout
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')

def homepage():
   # logging.basicConfig(filename="mywebapp.log", level=logging.DEBUG)
   # logging.debug("Program starts running at %d", time.time())
    logger.debug("Enter homepage **********************");
    count = get_hit_count()    
    
    html = 'Hello there! I have been seen <b>{}</b> times.\n'.format(count) + '   <b><a href="/">Hit me</a></b>' 
    ## Demonstrate to connect to either a mysql db inside a container or outside a container which is of the host machine
    dbFromContainer = count % 2 == 0;
    html = loadData(html, dbFromContainer);
    
    return html
    
def loadData(html, dbFromContainer):
    logger.debug("Load data from db in the container: {}".format(dbFromContainer));
    if dbFromContainer:
        connId = 'connection_from_container' 
    else:
        connId = 'connection_from_host'
        
    connection = ''    
    with open('mysql.yml') as stream:
        config = yaml.safe_load(stream)
        connection = config[connId];

    cnx = mysql.connector.connect(**connection)
    if cnx and cnx.is_connected():
        html+= "<p>Open DB connection OK."
        
        if dbFromContainer:
            
            html+= "<p>Connected to <u>MySql from docker container.</u>"
            
            sqlQry = "SELECT CURRENT_TIME(), quote FROM testdb.Quote;"
            html += "<p>Running SQL: <b> " + sqlQry + "</b><br><br>"
            with cnx.cursor() as cursor:
                result = cursor.execute(sqlQry)
                rows = cursor.fetchall()
                for r in rows:
                    line = "<li>{} :: {}".format(r[0], r[1])
                    html += line             
        else:
            
            html+= "<p>Connected to <u>MySql from host machine.</u>" 
            
            sqlQry = "SELECT NAME, DISTRICT, POPULATION FROM CITY WHERE COUNTRYCODE = 'CAN' ORDER BY POPULATION DESC; ";
            html += "<p>Running SQL: <b> " + sqlQry + "</b><br><br>"
            
            html += "<table><tr><th align='left'>City</th><th align='left'>Province</th><th align='left'>Population</th></tr>"
            with cnx.cursor() as cursor:
                result = cursor.execute(sqlQry)
                rows = cursor.fetchall()
                for r in rows:
                    line = "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(r[0], r[1], r[2])
                    html += line

            html += "</table>"
        
        cnx.close()
        
    else:
        html += "<p>Could not connect to MySQL DB"
        
    return html
