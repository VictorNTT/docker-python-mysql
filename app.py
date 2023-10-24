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

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

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
    count = get_hit_count()
    html = 'Hello World! I have been seen <b>{}</b> times.\n'.format(count) + '   <b><a href="/">Hit me</a></b>'    
    html = loadDataFromSQL(html)
    return html
    
def loadDataFromSQL(html):
    connection = ''

    with open('mysql.yml') as stream:
        config = yaml.safe_load(stream)
        connection = config['connection'];

    cnx = mysql.connector.connect(**connection)
     
    if cnx and cnx.is_connected():

        html+= "<p>Open connection OK"
        #sqlQry = "SELECT host, user FROM user";
        sqlQry = "select name, district, population from city where countrycode = 'CAN' order by population desc; ";
        html += "<p>Running SQL: <b> " + sqlQry + "</b><br><br>"
        
        html += "<table><tr><th align='left'>City</th><th align='left'>Province</th><th align='left'>Population</th></tr>"
        with cnx.cursor() as cursor:
            result = cursor.execute(sqlQry)
            rows = cursor.fetchall()
            for r in rows:
                line = "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(r[0], r[1], r[2])
                html += line

        html += "</table>"
        html += "<p><br>Close DB connection"
        cnx.close()

    else:
         html += "<p>Could not connect to MySQL DB"
    
    return html