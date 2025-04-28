# Renewable Energy Data Engineering Pipeline

## Project Overview
This project presents a complete data engineering workflow for renewable energy data from Germany. It demonstrates the ingestion of cleaned energy generation data into Kafka, storage into Railway PostgreSQL, ETL processing with Python, and dynamic visualization through a Flask dashboard.

## Tech Stack
- Kafka: Real-time data ingestion
- Zookeeper: Kafka cluster coordination
- Railway PostgreSQL: Cloud-based relational database storage
- Python: ETL processing and analysis (Pandas, SQLAlchemy, psycopg2)
- Flask: Lightweight web dashboard for visualizations
- DBeaver: GUI for database management
- Docker & Docker Compose: For containerizing Kafka and Zookeeper services

## Project Architecture
![arcnitecture](https://github.com/user-attachments/assets/32fa9ef9-ffa8-4898-834b-290c90df7f45)


## Features
- Real-time streaming of renewable energy data using Kafka
- Reliable cloud storage with PostgreSQL (Railway)
- Data cleaning, aggregation (daily/monthly) with Python
- Forecasting energy trends using time-series models
- Interactive dashboard built with Flask for visualization
- Dockerized local environment setup for Kafka and Zookeeper

## Folder Structure
```bash
+-- producer.PY
+-- consumer.PY
+-- main.py
+-- static
�   +-- graphs/
�       +-- energy_by_type_stacked.png
�       +-- energy_forecast.png
�       +-- individual_trend.png
�       +-- total_energy_line.png
+-- templates
�   +-- index.html
+-- app.py
+-- dockerfile
+-- docker-compose.yml
+-- requirements.txt
+-- .env.example
+-- README.md
+-- architecture.png
```

## How to Run the Project

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/renewable-energy-pipeline.git
cd renewable-energy-pipeline
```

### 2. Environment Setup
Create a `.env` file based on `.env.example`:
```bash
DB_HOST=your-railway-db-host
DB_PORT=5432
DB_USER=your-username
DB_PASSWORD=your-password
DB_NAME=your-db-name
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start Kafka and Zookeeper (Locally using Docker Compose)
```bash
docker-compose up -d
```

### 5. Run Kafka Producer
```bash
python producer/kafka_producer.py
```

### 6. Run Kafka Consumer
```bash
python consumer/kafka_consumer.py
```

### 7. Perform ETL and Analysis
```bash
python etl/data_etl.py
```

### 8. Start Flask Dashboard
```bash
cd flask_app
python app.py
```
Then open your browser at: [http://localhost:5000](http://localhost:5000)

