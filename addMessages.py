import pika, os

url = os.environ.get('CLOUDAMQP_URL', 'amqps://ietfgcja:mO2moIbKdiKWUNlcM8Ck7VlzvcYYDvMg@shark.rmq.cloudamqp.com/ietfgcja')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='forecasts') # Declare a queue

cities = ["New York", "Los Angeles", "Houston", "Seattle", "Savannah", "Oakland", "Charleston", "Norfolk", "Miami", "Port Everglades", "Tacoma", "New Orleans", "Baltimore", "Jacksonville", "Philadelphia", "San Juan", "San Diego", "Boston", "Mobile", "Long Beach", "Port Hueneme", "Wilmington", "Corpus Christi", "Portland", "Tampa", "Anchorage", "Beaumont", "Honolulu", "Newark", "Richmond", "Palm Beach", "Galveston", "Brownsville", "Port Arthur", "Detroit", "Chicago", "Baton Rouge", "Memphis", "Laredo", "Buffalo", "Cleveland", "Cincinnati", "Louisville",  "St Paul", "Pittsburgh", "Albany", "Oklahoma City", "St Louis"]
#cities = ["New York", "Los Angeles"]
#cities = ["New York"]
for city in cities:
  channel.basic_publish(exchange='',
                      routing_key='forecasts',
                      body=city)
  print(" [x] Sent "+city)
connection.close()



