# set up and dependencies
from tkinter.tix import COLUMN
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy import func
from flask import Flask, jsonify

# Database Setup
#################################################
Base = declarative_base() 

#create class for measurement table
class measurement(Base):
    __tablename__ = "measurement"
    
    id = Column(Integer, primary_key=True)
    station = Column(String)
    date = Column(Date)
    prcp = Column(Float)
    tobs = Column(Float)


#creating class for station table
class station(Base):
    __tablename__ = "station"
    
    id = Column(Integer, primary_key=True)
    station = Column(String)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation =  Column(Float)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
session = scoped_session(sessionmaker(bind=engine))


# establishing the app
app = Flask(__name__)


# Home page route
@app.route("/")
def main():
    return (
        f"Welcome! This is the Climate App Home Page! <br>"
        f"Available Routes can be found Below:<br>"
        f"Precipitation measurement over the last 12 months: /api/v1.0/precipitation<br>"
        f"A list of stations and their station numbers: /api/v1.0/stations<br>"
        f"Temperature observations for the most active station within the last 12 months: /api/v1.0/tobs<br>"
        f"Enter a start date (yyyy-mm-dd) to get the minimum, maximum, and average temperatures for all dates after a specified date: /api/v1.0/<start><br>"
        f"Enter both a start and end date (yyyy-mm-dd) to get the minimum, maximum, and average temperatures for the date range: /api/v1.0/<start>/<end><br>"
    )


# precipitation route of last 12 months of precipitation data
# /api/v1.0/precipitation
# Convert the query results to a dictionary by using date as the key and prcp as the value.

# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precip():

    recent_prcp = session.query(str(measurement.date), measurement.prcp)\
    .filter(measurement.date > '2016-08-22')\
    .filter(measurement.date <= '2017-08-23')\
    .order_by(measurement.date).all()

    # converting results to a dictionary with date as key and prcp as value
    prcp_dict = dict(recent_prcp)

  
    return jsonify(prcp_dict)

# creating station route of a list of the stations in the dataset
# /api/v1.0/stations
# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():

    stations = session.query(station.name, station.station).all()

    # converting results to a dict
    stations_dict = dict(stations)

    
    return jsonify(stations_dict)

# creating tobs route of temp observations for most active station over last 12 months
# /api/v1.0/tobs
# Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():

    tobs_station = session.query(str(measurement.date), measurement.tobs)\
    .filter(measurement.date > '2016-08-23')\
    .filter(measurement.date <= '2017-08-23')\
    .filter(measurement.station == "USC00519281")\
    .order_by(measurement.date).all()

    # creating dict
    tobs_dict = dict(tobs_station)

    
    return jsonify(tobs_dict)




# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_date(start, end=None):

    q = session.query(str(func.min(measurement.tobs)), str(func.max(measurement.tobs)), str(func.round(func.avg(measurement.tobs))))

    if start:
        q = q.filter(measurement.date >= start)

    if end:
        q = q.filter(measurement.date <= end)
   

    results = q.all()[0]

    keys = ["Min Temp", "Max Temp", "Avg Temp"]

    temp_dict = {keys[i]: results[i] for i in range(len(keys))}

    return jsonify(temp_dict)


if __name__ == "__main__":
    app.run(debug=True)