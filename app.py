#Dependencies 
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, inspect, func
from sqlalchemy import distinct
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify
import datetime as dt


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

measurement = Base.classes.measurement
station = Base.classes.station


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


#Home Page
@app.route("/")
def home():
    return (
        f"Welcome to the Homework API Home Page!<br>"
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/yyyy-mm-dd<br>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br>"
        f"Please copy the format above to check the temps for the dates"                              
    )

#Precipitation
@app.route("/api/v1.0/precipitation")
def precipiation():
    #Open session and query
    session = Session(engine)
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results =session.query(measurement.date, measurement.prcp).\
    filter(measurement.date > year_ago).\
    order_by(measurement.date).all()

    #Close session
    session.close()

    #Dictionary
    precipitation = []
    for date, prcp in results:
        dict = {}
        dict["date"] = date
        dict["prcp"] = prcp
        precipitation.append(dict)

    return jsonify(precipitation)


#Stations
@app.route("/api/v1.0/stations")
def station():
    #Open session and query
    session = Session(engine)

    results = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()

    stations = list(np.ravel(results))
   
    #Close session
    session.close()


    return jsonify(stations)



#TOBS
@app.route("/api/v1.0/tobs")
def tobs():
    #Open session and query
    session = Session(engine)

    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    query =session.query(measurement.tobs).\
    filter(measurement.date >= year_ago).\
    filter(measurement.station == 'USC00519281').all()

    tobs = list(np.ravel(query))

    #Close session
    session.close()


    return jsonify(tobs)


#Dates
@app.route("/api/v1.0/<start_date>")
def date(start_date):

    #Open session and query
    session = Session(engine)

    temps1 = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).all()
    #Close session
    session.close()


    return jsonify(temps1)

#Dates
@app.route("/api/v1.0/<start_date>/<end_date>")
def date2(start_date, end_date):

    #Open session and query
    session = Session(engine)

    temps2 = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    #Close session
    session.close()


    return jsonify(temps2)





if __name__ == '__main__':
    app.run(debug=True)
