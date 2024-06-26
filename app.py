#!/usr/bin/env python3
import os
import requests
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://uahr1t8mhbh2ou:p37de180475ed61ab5fa6d80a4d446a1c7135e89607020eae8dc5f7d4e34caf5b@cd1goc44htrmfn.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d5ukmvbbr0hl1d'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Forecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    avg_temp = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    wind_direction = db.Column(db.String(5), nullable=False)
    condition = db.Column(db.String(100), nullable=False)
    swell_ht_ft = db.Column(db.Float)
    hour = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())


    def __repr__(self):
        return f'<Forecast {self.location}>'




with app.app_context():
    db.create_all()


def deleteForecasts():
   delete_forecasts = Forecast.query.delete()
   return delete_forecasts

@app.route("/")
def main():
    return '''
     <h1> Data Collector</h1>

     '''


@app.route('/show_data/<int:id>')
def dbCall(id):

    get_forecast = db.get_or_404(Forecast,id)

    return "Data pulled from DB for record ID:"+str(get_forecast.id)+"<br> port name:"+str(get_forecast.location)\
    +"<br> weather condition: "+get_forecast.condition \
    +"<br> average temp F: "+str(get_forecast.avg_temp)\
    +"<br> wind speed: "+str(get_forecast.wind_speed) \
    +"<br> wind direction: "+get_forecast.wind_direction \
    +"<br> swell height ft: "+str(get_forecast.swell_ht_ft)


@app.route('/show_all_data')
def dbCallAll():
    get_forecasts = Forecast.query.all()
    print(get_forecasts)
    return "got data"
    return "Data pulled from DB for record ID:"+str(get_forecast.id)+"<br> port name:"+str(get_forecast.location)\
    +"<br> weather condition: "+get_forecast.condition \
    +"<br> average temp F: "+str(get_forecast.avg_temp)\
    +"<br> wind speed: "+str(get_forecast.wind_speed) \
    +"<br> wind direction: "+get_forecast.wind_direction \
    +"<br> swell height ft: "+str(get_forecast.swell_ht_ft)


@app.route('/pull_data')
def apiCall():
    delete_forecasts = deleteForecasts()
    print(delete_forecasts, "deleted")
    db.session.commit()
    cities = ["New York", "Los Angeles", "Houston", "Seattle", "Savannah", "Oakland", "Charleston", "Norfolk", "Miami", "Port Everglades", "Tacoma", "New Orleans", "Baltimore", "Jacksonville", "Philadelphia", "San Juan", "San Diego", "Boston", "Mobile", "Long Beach", "Port Hueneme", "Wilmington", "Corpus Christi", "Portland", "Tampa", "Anchorage", "Beaumont", "Honolulu", "Newark", "Richmond", "Palm Beach", "Galveston", "Brownsville", "Port Arthur", "Detroit", "Chicago", "Baton Rouge", "Memphis", "Laredo", "Buffalo", "Cleveland", "Cincinnati", "Louisville",  "St Paul", "Pittsburgh", "Albany", "Oklahoma City", "St Louis"]

    for city in cities:
       response = requests.get('http://api.weatherapi.com/v1/marine.json?key=83630e43f1404792967173131241606&q='+city+'&days=1')
       forecast_response = response.json()
       print(forecast_response['forecast']['forecastday'][0]['day']['avgtemp_f'])
       forecast = Forecast( location=forecast_response['location']['name'], \
     avg_temp=forecast_response['forecast']['forecastday'][0]['day']['avgtemp_f'], \
     wind_speed=forecast_response['forecast']['forecastday'][0]['hour'][0]['wind_mph'], \
     wind_direction=forecast_response['forecast']['forecastday'][0]['hour'][0]['wind_dir'], \
     condition=forecast_response['forecast']['forecastday'][0]['hour'][0]['condition']['text'], \
     swell_ht_ft=forecast_response['forecast']['forecastday'][0]['hour'][0]['swell_ht_ft'], \
     hour=0 )
       print("PULLING DATA FOR",forecast_response['location']['name'])
       print(forecast)
       db.session.add(forecast)
       db.session.commit()

    return "Pulling data from http://api.weatherapi.com <br>Forecast Data Written to DB ID:"+str(forecast.id)+"<br>click link to pull data from DB for this record <a href='./show_data/"+str(forecast.id)+"' > pull data from DB</a>"


