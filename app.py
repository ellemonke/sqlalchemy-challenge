import numpy as np
import datetime as dt

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
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&#60;start_date&#62;<br/>"
        f"/api/v1.0/&#60;start_date&#62;/&#60;end_date&#62;<br/>"
        f"<br/>Note: Date format should be YYYY-MM-DD."
    )


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations including the station, name, latitude, longitude and elevation of each station"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    station_results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station, name, latitude, longitude, elevation in station_results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a dictionary of average precipitation for each day"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for the dates and average precipitation
    prcp_results = session.query(Measurement.date, func.avg(Measurement.prcp)).group_by(Measurement.date).all()

    session.close()

    # Create a dictionary from the result data
    prcp_dict = {}
    for date, prcp in prcp_results:
        prcp_dict[date] = prcp

    return jsonify(prcp_dict)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a dictionary of average precipitation for each day, one year from the last date"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for the last day in the data set    
    last_day = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # Convert result object to string
    last_day = last_day.date   
    # Convert string to datetime object
    last_day_obj = dt.datetime.strptime(last_day, '%Y-%m-%d')

    # Calculate one year ago
    year_ago = last_day_obj - dt.timedelta(days=365)
    # Convert date object to string
    year_ago = year_ago.strftime("%Y-%m-%d")

    # Query for the dates and average temperatures for one year from the last data point.
    tobs_results = session.query(Measurement.date, func.avg(Measurement.tobs)).\
        filter(Measurement.date > year_ago).\
        group_by(Measurement.date).all()

    session.close()

    # Create a dictionary from the result data
    tobs_dict = {}
    for date, tobs in tobs_results:
        tobs_dict[date] = tobs

    return jsonify(tobs_dict)


@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature starting at a given date."""
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query for the TMIN, TAVG and TMAX starting from the given date
    tobs_stats = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    # Convert results to a list
    tobs_stats = list(np.ravel(tobs_stats))

    session.close()
    
    if tobs_stats[0] is None:
        return jsonify({"error": f"Sorry, the date '{start_date}' was not found."}), 404

    # Create a dictionary from the result data
    stats_dict = {
        'Min Temp' : tobs_stats[1],
        'Avg Temp' : tobs_stats[2],
        'Max Temp' : tobs_stats[3]
    }

    return jsonify(stats_dict)


@app.route("/api/v1.0/<start_date>/<end_date>")
def all_dates(start_date, end_date):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature between a given start date and end date."""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for the TMIN, TAVG and TMAX within the given date range
    tobs_range_stats = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    # Convert results to a list
    tobs_range_stats = list(np.ravel(tobs_range_stats))

    # Query for the first day in the data set    
    first_day = session.query(Measurement.date).order_by(Measurement.date).first()
    # Convert results to a string
    first_day_str = first_day.date

    # Query for the last day in the data set    
    last_day = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # Convert results to a string
    last_day_str = last_day.date

    session.close()

    # Convert date strings to datetime objects for comparison
    first_day = dt.datetime.strptime(first_day_str, '%Y-%m-%d')
    last_day = dt.datetime.strptime(last_day_str, '%Y-%m-%d')
    start_date = dt.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end_date, '%Y-%m-%d')

    # Check if given dates are within range
    if (first_day <= start_date < last_day) and (first_day < end_date <= last_day):

        # Create a dictionary from the result data
        range_stats_dict = {
            'Min Temp' : tobs_range_stats[1],
            'Avg Temp' : tobs_range_stats[2],
            'Max Temp' : tobs_range_stats[3]
        }

        return jsonify(range_stats_dict)
    
    else:
        return jsonify({"error": f"Please enter a date after {first_day_str} and before {last_day_str}."}), 404


# Preview on 127.0.0.1:5000
if __name__ == '__main__':
    app.run(debug=True, port=5000)
