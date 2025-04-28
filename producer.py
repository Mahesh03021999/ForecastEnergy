import pandas as pd
from kafka import KafkaProducer
import json
import time

# Kafka Producer setup
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Load and clean Excel data
def load_energy_data(file_path):
    df = pd.read_excel(file_path, skiprows=6)
    df.replace('-', pd.NA, inplace=True)
    numeric_cols = ['Total[MWh]', 'Wind offshore[MWh]', 'Wind onshore[MWh]', 'Photovoltaics[MWh]', 'Other[MWh]']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    df['timestamp'] = pd.to_datetime(df['Date'] + ' ' + df['Time of day'], errors='coerce')
    df.dropna(subset=['timestamp'], inplace=True)
    return df[['timestamp'] + numeric_cols]

def send_data_to_kafka(df):
    for _, row in df.iterrows():
        message = {
            'timestamp': row['timestamp'].isoformat(),
            'total_mwh': row['Total[MWh]'],
            'wind_offshore': row['Wind offshore[MWh]'],
            'wind_onshore': row['Wind onshore[MWh]'],
            'photovoltaics': row['Photovoltaics[MWh]'],
            'other': row['Other[MWh]']
        }
        producer.send('energy_topic', value=message)
        print(f"📤 Sent: {message}")
    producer.flush()
    print("✅ All messages sent!")

if __name__ == "__main__":
    df = load_energy_data("Forecasted_generation_202101010000_202112312359.xlsx")
    send_data_to_kafka(df)
