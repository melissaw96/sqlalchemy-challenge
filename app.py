# Import the dependencies.

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session from Python to DB
    session = Session(engine)
    # Convert query results from precipitation analysis to a dictionary using date as key and prcp as value
    precipitation_query = session.query(Measurement.prcp, Measurement.date).all()

    session.close()

    precipitation = []
    for prcp, date in precipitation_query:
        precipitation_dict = {}
        precipitation_dict["prcp"] = prcp
        precipitation_dict["date"] = date 
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session from Python to DB 
    session = Session(engine)
    # Return JSON list of stations 
    stations_query = session.query(Station.station,Station.id).all()
    
    session.close()

    stations = []
    for station, id in stations_query:
        stations_dict = []
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["id"] = id 
        stations.append(stations_dict)


    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session from Python to DB 
    session = Session(engine)
    # Query dates and temp observations of most-active station for previous year of data
    most_active_station_query = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).\
                            filter(Measurement.date >= '2016-08-23').\
                            filter(Measurement.station == 'USC00519281').\
                            order_by(Measurement.date).all()
    
    session.close()

    most_active_station = []
    for date, tobs, prcp in most_active_station_query: 
        most_active_station_dict = {}
        most_active_station_dict["date"] = date
        most_active_station_dict["tobs"] = tobs
        most_active_station_dict["prcp"] = prcp 
        most_active_station.append(most_active_station_dict)

    return jsonify(most_active_station)


@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session 
    session = Session(engine)
    # Return JSON list of min, avg, and max temp for a specified start or start-end range
    start_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start).all()
    
    session.close()

    start_date_tobs = []
    for min, avg, max in start_query:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min
        start_date_tobs_dict["avg_temp"] = avg 
        start_date_tobs_dict["max_temp"] = max 
        start_date_tobs.append(start_date_tobs_dict)

    return jsonify(start_date_tobs)


@app.route("/api/v1.0/<start>/<end>")
def end_date(end):
    # Create session 
    session = Session(engine)
    # Calculate TMIN, TAVG, TMAX for all dates greater than or equal to the start date 
    # For specified start and end date, calculate TMIN, TAVG, and TMAX from start date to end date inclusive
    end_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start_date).\
                        filter(Measurement.date <= end_date).all()
    session.close()

    start_end_date_tobs = []
    for min, avg, max in end_query:
        start_end_date_tobs_dict = {}
        start_end_date_tobs_dict["min_temp"] = min
        start_end_date_tobs_dict["avg_temp"] = avg
        start_end_date_tobs_dict["max_temp"] = max
        start_end_date_tobs.append(start_end_date_tobs_dict)

    return jsonify(start_end_date_tobs)


if __name__ == '__main__':
    app.run(debug=True)








                                        
                                        