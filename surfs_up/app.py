#1) IMPORT DEPENDENCIES

import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#2) SET UP THE DATABASE
#access the database
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()

# add code to reflect the database
Base.prepare(engine, reflect=True)

#create variables to hold each class
Measurement = Base.classes.measurement
Station = Base.classes.station

#create a session linke from python to database
session = Session(engine)

#3)SET UP FLASK
#define flask app
app = Flask(__name__)

#below example is if we want to run in another python
#import app
#print("example __name__ = %s", __name__)
#if __name__ == "__main__":
   # print("example is being run directly.")
#else:
    #print("example is being imported")

#4) CREATE THE WELCOME ROUTE
#define the welcome route
@app.route('/')
#add routing information for each of the other routes
#create welcome
def welcome():
    return(
        #add precipitation, stations, tobs, & temp routes
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

#5) CREATE PRECIPITATION ROUTE
@app.route("/api/v1.0/precipitation")
def precipitation():
    #calculate the date from a year ago from the most recent date
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #write a query
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#6) CREATE STATIONS ROUTE
@app.route("/api/v1.0/stations")
def stations():
    #create a query to get all the stations
    results = session.query(Station.station).all()
    # convert results into a list
    stations = list(np.ravel(results))
    #return list as JSON by adding stations=stations
    return jsonify(stations=stations)

#7) MONTHLY TEMPERATURE ROUTE
@app.route("/api/v1.0/tobs")
def temp_monthly():
# calculate date one year ago from last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #query primary station for all temps from prev year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
#unravel results into one dimensional array and convert to a list
    temps = list(np.ravel(results))
#Jsonify the temps
    return jsonify(temps=temps)

#8) STATISTICS ROUTE
# get max, min and avg temps
#create the routes
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
#create the function, add parameters
def stats(start=None, end=None):
    #create query to select min, avg, and max temps from SQLite
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
# add an if-not statement to detmerin start and end
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)
    #calculate the temp min, avd and max with the start and end dates
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

