# 1. import Dependencies


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# Home page.

  # List all routes that are available.

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/start/end/<start>/<end><br/>"
        f"Start and End Date Format yyyy-mm-dd"
    )
# 3. Define what to do when a user hits the index route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Convert the query results to a dictionary using 
    # `date` as the key and `prcp` as the value.
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    
    # Return the JSON representation of your dictionary.
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    station_results = session.query(Station.name).all()

    session.close()

    all_stations = list(np.ravel(station_results))
    # Return a JSON list of stations from the dataset.
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    # Query the dates and temperature observations of the 
    # most active station for the last year of data.
      
    tobs = session.query(Measurement.tobs).filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station == 'USC00519281').all()

    session.close()

    tobs_list = list(np.ravel(tobs))
    # Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(tobs_list)

#@app.route("/api/v1.0/<start>" and "/api/v1.0/,start>/<end>")
@app.route("/api/v1.0/start/<start>")
@app.route("/api/v1.0/start/end/<start>/<end>")
def temp(start= None, end= None):
    start_date = start
    end_date = end

    session = Session(engine)

    if end_date == None:
        MaxTemp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).scalar() 

        MinTemp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).scalar()
    
        AveTemp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).scalar()

    else:

        MaxTemp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).scalar() 

        MinTemp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).scalar()
    
        AveTemp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).scalar()
    
    session.close()

    temp_date = []
    temp_date_dict = {}
    temp_date_dict["Start_Date"] = start_date
    temp_date_dict["End_Date"] = end_date
    temp_date_dict["Max_Temp"] = MaxTemp
    temp_date_dict["Min_Temp"] = MinTemp
    temp_date_dict["Avg_Temp"] = round(AveTemp, 2)
    temp_date.append(temp_date_dict)

    return jsonify(temp_date)
 


if __name__ == '__main__':
    app.run(debug=True)
session.close()