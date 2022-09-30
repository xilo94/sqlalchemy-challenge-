# set up and dependencies
from lib2to3.pytree import _Results
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base() 
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():

    """List all available API routes."""

    return (
    f"Welcome! This is the SQL-Alchemy APP API!<br/>"
    f"Available Routes can be found here:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
    f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
 # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Precipitation Data"""
# Query all Precipitation
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= "2016-08-23").\
        all()

    session.close()

# Convert the list to Dictionary
    prcp_all_dict = []
    for date,prcp  in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
               
        prcp_all_dict.append(prcp_dict)

    return jsonify(prcp_all_dict)


@app.route("/api/v1.0/stations")
def stations():

# Create session

    session = Session(engine)

    """Return a list of all Stations"""

# Query all Stations

    results = session.query(station.station).\
                 order_by(station.station).all()

    session.close()

# Convert list of tuples into normal list

    stations_all = list(np.ravel(results))

    return jsonify(stations_all)

@app.route("/api/v1.0/tobs")
def tobs():
# Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all TOBs"""
# Query all tobs

    results = session.query(measurement.date,  measurement.tobs,measurement.prcp).\
    filter(measurement.date >= '2016-08-23').\
    filter(measurement.station=='USC00519281').\
    order_by(measurement.date).all()

    session.close()

   

# Convert the list to Dictionary

    tobs_all_dict = []
    for prcp, date, tobs in results:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs

        tobs_all_dict.append(tobs_dict)
    return jsonify(tobs_all_dict)
    
@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):
 
 # Create our session 
 
    session = Session(engine)

    """Return a list of min, avg and max tobs for a start date"""

# Query all tobs

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start_date).all()

    session.close()

# Create a dictionary from the row data and append to a list of start_date_tobs

    start_date_tobs = []

    for min, avg, max in results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min
        start_date_tobs_dict["avg_temp"] = avg
        start_date_tobs_dict["max_temp"] = max
        start_date_tobs.append(start_date_tobs_dict) 
    return jsonify(start_date_tobs)

@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):

# Create our session (link) from Python to the DB

session = Session(engine)

"""Return a list of min, avg and max tobs for start and end dates"""
# Query all tobs

results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
        
session.close()
  
# Create a dictionary from the row data and append to a list of start_end_date_tobs

start_end_tobs = []
for min, avg, max in results:
    start_and_end_tobs_dict = {}
    start_and_end_tobs_dict["min_temp"] = min
    start_and_end_tobs_dict["avg_temp"] = avg
    start_and_end_tobs_dict["max_temp"] = max
    start_and_end_tobs_dict.append(start_and_end_tobs_dict) 
    
return jsonify(start_and_end_tobs_dict)

if __name__ == "__main__":
    app.run(debug=True)