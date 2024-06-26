import pika, os
import requests
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://uahr1t8mhbh2ou:p37de180475ed61ab5fa6d80a4d446a1c7135e89607020eae8dc5f7d4e34caf5b@cd1goc44htrmfn.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d5ukmvbbr0hl1d'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

url = os.environ.get('CLOUDAMQP_URL', 'amqps://ietfgcja:mO2moIbKdiKWUNlcM8Ck7VlzvcYYDvMg@shark.rmq.cloudamqp.com/ietfgcja')

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

params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() 
channel.queue_declare(queue='forecasts') 

def callback(ch, method, properties, body):
  city = body.decode('ASCII')
  print(" [x] Received " + city)
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
  with app.app_context():
     db.session.add(forecast)
     db.session.commit()


channel.basic_consume('forecasts',
                      callback,
                      auto_ack=True)

print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()
