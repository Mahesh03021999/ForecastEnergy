from kafka import KafkaConsumer
import json
import psycopg2
from urllib.parse import urlparse

# PostgreSQL setup
DATABASE_URL = "postgresql://postgres:LxbHTuXlGffdkdNGtwwMaOIvPkjAXYaE@metro.proxy.rlwy.net:36911/railway"
url = urlparse(DATABASE_URL)

# Connect to DB
conn = psycopg2.connect(
    host=url.hostname,
    database=url.path[1:],
    user=url.username,
    password=url.password,
    port=url.port
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS energy_generation (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP UNIQUE,
    total_mwh FLOAT,
    wind_offshore FLOAT,
    wind_onshore FLOAT,
    photovoltaics FLOAT,
    other FLOAT
)
""")
conn.commit()

# Kafka Consumer setup
consumer = KafkaConsumer(
    'energy_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='energy_group'
)

print("🕵️‍♂️ Listening for messages...")

for message in consumer:
    data = message.value
    print(f"📥 Received: {data}")
    try:
        cursor.execute("""
            INSERT INTO energy_generation (timestamp, total_mwh, wind_offshore, wind_onshore, photovoltaics, other)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (timestamp) DO NOTHING
        """, (
            data['timestamp'],
            data['total_mwh'],
            data['wind_offshore'],
            data['wind_onshore'],
            data['photovoltaics'],
            data['other']
        ))
        conn.commit()
        print(f"✅ Inserted into DB: {data['timestamp']}")
    except Exception as e:
        print(f"❌ DB insert error: {e}")
