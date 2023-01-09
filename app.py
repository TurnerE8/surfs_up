# Import dependencies 
import datetime as dt 
import numpy as np
import pandas as pd 

# Import dependencies needed for SQLAlchemy 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base 
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func 

# Import dependencies needed for Flask 
from Flask import Flask, jsonify 

# Set up database engine for the Flask application 
engine = create_engine("sqlite://hawaii")

# Reflect the database into our classes 
Base = automap_base
Base.prepare(engine, reflect=True)

# Create a variable for each of the classes 
Measurement = Base.classes.measurement 
Station = Base.classes.station 

# Create the session link from Python to the database: 
session = Session(engine)

###NEXT, WE SET UP OUR FLASK APPLICATION 

#Set up Flask 
app = Flask(__name__)
#STOPPED AT 9.5.2 "Create the Welcome Route"
@app.route("/")

#add the routing information for each of the roots
def welcome():
    return( 
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

@app.route("/api/v1.0/precipitation")

def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}    
    return jsonify(precip)

@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)