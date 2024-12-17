from app import initialize_app

app = initialize_app()
if __name__=='__main__':
    app.run(debug=True) 
    
# Data Consumer (Microservice 2 - Kafka to Redis)

from kafka import KafkaConsumer
import redis
import json

consumer = KafkaConsumer(
    'equity_market_data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

for message in consumer:
    data = message.value
    redis_client.rpush('market_data', json.dumps(data))
    print(f"Stored in Redis: {data}")
