#!/usr/bin/env python3
import os
import requests
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import pika

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://uahr1t8mhbh2ou:p37de180475ed61ab5fa6d80a4d446a1c7135e89607020eae8dc5f7d4e34caf5b@cd1goc44htrmfn.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d5ukmvbbr0hl1d'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

url = os.environ.get('CLOUDAMQP_URL', 'amqps://ietfgcja:mO2moIbKdiKWUNlcM8Ck7VlzvcYYDvMg@shark.rmq.cloudamqp.com/ietfgcja')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='forecasts') # Declare a queue

class Forecasts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    day = db.Column(db.String(50), nullable=False)
    day_condition = db.Column(db.String(100))
    day_condition_icon = db.Column(db.String(100)) 
    h1_avg_temp = db.Column(db.Float)
    h1_wind_speed = db.Column(db.Float)
    h1_wind_direction = db.Column(db.String(5), nullable=False)
    h1_swell_ht_ft = db.Column(db.Float)
    h1_avg_temp = db.Column(db.Float)
    h1_wind_speed = db.Column(db.Float)
    h1_wind_direction = db.Column(db.String(5), nullable=False)
    h1_swell_ht_ft = db.Column(db.Float)
    h2_avg_temp = db.Column(db.Float)
    h2_wind_speed = db.Column(db.Float)
    h2_wind_direction = db.Column(db.String(5), nullable=False)
    h2_swell_ht_ft = db.Column(db.Float)
    h3_avg_temp = db.Column(db.Float)
    h3_wind_speed = db.Column(db.Float)
    h3_wind_direction = db.Column(db.String(5), nullable=False)
    h3_swell_ht_ft = db.Column(db.Float)
    h4_avg_temp = db.Column(db.Float)
    h4_wind_speed = db.Column(db.Float)
    h4_wind_direction = db.Column(db.String(5), nullable=False)
    h4_swell_ht_ft = db.Column(db.Float)
    h5_avg_temp = db.Column(db.Float)
    h5_wind_speed = db.Column(db.Float)
    h5_wind_direction = db.Column(db.String(5), nullable=False)
    h5_swell_ht_ft = db.Column(db.Float)
    h6_avg_temp = db.Column(db.Float)
    h6_wind_speed = db.Column(db.Float)
    h6_wind_direction = db.Column(db.String(5), nullable=False)
    h6_swell_ht_ft = db.Column(db.Float)
    h7_avg_temp = db.Column(db.Float)
    h7_wind_speed = db.Column(db.Float)
    h7_wind_direction = db.Column(db.String(5), nullable=False)
    h7_swell_ht_ft = db.Column(db.Float)
    h8_avg_temp = db.Column(db.Float)
    h8_wind_speed = db.Column(db.Float)
    h8_wind_direction = db.Column(db.String(5), nullable=False)
    h8_swell_ht_ft = db.Column(db.Float)
    h9_avg_temp = db.Column(db.Float)
    h9_wind_speed = db.Column(db.Float)
    h9_wind_direction = db.Column(db.String(5), nullable=False)
    h9_swell_ht_ft = db.Column(db.Float)
    h10_avg_temp = db.Column(db.Float)
    h10_wind_speed = db.Column(db.Float)
    h10_wind_direction = db.Column(db.String(5), nullable=False)
    h10_swell_ht_ft = db.Column(db.Float) 
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<Forecasts {self.location}>'

with app.app_context():
    db.create_all()

def deleteForecasts():
   delete_forecasts = Forecasts.query.delete()
   return delete_forecasts

def deleteLocationForecasts(city):
   delete_forecasts = Forecasts.query.filter_by(location=city).delete()
   return delete_forecasts

def callback(ch, method, properties, body):
  print(" [x] Received " + str(body))
  city = body.decode('ASCII')
  response = requests.get('http://api.weatherapi.com/v1/marine.json?key=83630e43f1404792967173131241606&q='+city+'&days=5')
  forecast_response = response.json()
  print(forecast_response['forecast']['forecastday'][0]['day']['avgtemp_f'])
  location = forecast_response['location']['name']
  with app.app_context():
    svs = Forecasts.query.filter_by(location=location).delete()
    print(svs)
    db.session.commit()
    print('deleted', location)
  with app.app_context():  
    deleteLocationForecasts(location)
  days = forecast_response['forecast']['forecastday']
  for day in days:
      day_date = day['date']
      day_condition = day['day']['condition']['text']
      day_condition_icon = day['day']['condition']['icon']
      day_hours = day['hour']
      i = 0
      for hour in day_hours:
         globals()[f"hour_{i}_temp"]=hour['temp_f'] 
         globals()[f"hour_{i}_wind_speed"]=hour['wind_mph']
         globals()[f"hour_{i}_wind_direction"]=hour['wind_dir']
         globals()[f"hour_{i}_waves"]=hour['swell_ht_ft']
         i = i+1
      
      print("PULLING DATA FOR",forecast_response['location']['name'],day_date)
      forecast = Forecasts(\
   location = location,\
   day = day_date, \
   day_condition = day_condition, \
   day_condition_icon =  day_condition_icon,\
   h1_avg_temp = hour_7_temp, \
   h1_wind_speed = hour_7_wind_speed, \
   h1_wind_direction = hour_7_wind_direction, \
   h1_swell_ht_ft = hour_7_waves, \
   h2_avg_temp = hour_8_temp, \
   h2_wind_speed = hour_8_wind_speed, \
   h2_wind_direction = hour_8_wind_direction, \
   h2_swell_ht_ft = hour_8_waves, \
   h3_avg_temp = hour_9_temp, \
   h3_wind_speed = hour_9_wind_speed, \
   h3_wind_direction = hour_9_wind_direction, \
   h3_swell_ht_ft = hour_9_waves, \
   h4_avg_temp = hour_10_temp, \
   h4_wind_speed = hour_10_wind_speed, \
   h4_wind_direction = hour_10_wind_direction, \
   h4_swell_ht_ft = hour_10_waves, \
   h5_avg_temp = hour_11_temp, \
   h5_wind_speed = hour_11_wind_speed, \
   h5_wind_direction = hour_11_wind_direction, \
   h5_swell_ht_ft = hour_11_waves, \
   h6_avg_temp = hour_12_temp, \
   h6_wind_speed = hour_12_wind_speed, \
   h6_wind_direction = hour_12_wind_direction, \
   h6_swell_ht_ft = hour_12_waves, \
   h7_avg_temp = hour_13_temp, \
   h7_wind_speed = hour_13_wind_speed, \
   h7_wind_direction = hour_13_wind_direction, \
   h7_swell_ht_ft = hour_13_waves, \
   h8_avg_temp = hour_14_temp, \
   h8_wind_speed = hour_14_wind_speed, \
   h8_wind_direction = hour_14_wind_direction, \
   h8_swell_ht_ft = hour_14_waves, \
   h9_avg_temp = hour_15_temp, \
   h9_wind_speed = hour_15_wind_speed, \
   h9_wind_direction = hour_15_wind_direction, \
   h9_swell_ht_ft = hour_15_waves, \
   h10_avg_temp = hour_16_temp, \
   h10_wind_speed = hour_16_wind_speed, \
   h10_wind_direction = hour_16_wind_direction, \
   h10_swell_ht_ft = hour_16_waves) 
      with app.app_context():
        
        svs = db.session.add(forecast)
        db.session.commit()
        print(svs)
        print( day_date , "DONE")
  print("test output",str(hour_4_waves))
channel.basic_consume('forecasts',
                      callback,
                      auto_ack=True)

print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()

