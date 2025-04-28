import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import psycopg2
from flask import Flask, render_template
from statsmodels.tsa.holtwinters import ExponentialSmoothing

plt.switch_backend('Agg')

app = Flask(__name__, template_folder='templates')

GRAPH_FOLDER = os.path.join(app.static_folder, 'graphs')
os.makedirs(GRAPH_FOLDER, exist_ok=True)

def fetch_monthly_data():
    conn = psycopg2.connect(
        host="metro.proxy.rlwy.net",
        port="36911",
        dbname="railway",
        user="postgres",
        password="LxbHTuXlGffdkdNGtwwMaOIvPkjAXYaE"
    )

    query = """
    SELECT 
        DATE_TRUNC('month', timestamp) AS month,
        SUM(COALESCE(wind_offshore, 0)) AS wind_offshore,
        SUM(COALESCE(wind_onshore, 0)) AS wind_onshore,
        SUM(COALESCE(photovoltaics, 0)) AS photovoltaics,
        SUM(COALESCE(other, 0)) AS other,
        SUM(
            COALESCE(wind_offshore, 0) + 
            COALESCE(wind_onshore, 0) + 
            COALESCE(photovoltaics, 0)
        ) AS total_mwh
    FROM energy_generation
    WHERE EXTRACT(YEAR FROM timestamp) = 2021
    GROUP BY month
    ORDER BY month
    """

    df = pd.read_sql(query, conn)
    df['month'] = pd.to_datetime(df['month']).dt.strftime('%Y-%m')
    df = df.fillna(0)
    return df

def plot_stacked_bar(df):
    plt.figure(figsize=(12, 6))
    plt.bar(df['month'], df['wind_onshore'], label='Wind Onshore', color='indigo')
    plt.bar(df['month'], df['wind_offshore'], bottom=df['wind_onshore'], label='Wind Offshore', color='teal')
    bottom_sum = df['wind_onshore'] + df['wind_offshore']
    plt.bar(df['month'], df['photovoltaics'], bottom=bottom_sum, label='Photovoltaics', color='gold')
    plt.xticks(rotation=45)
    plt.title("Energy Generation by Type (Wind Onshore, Offshore, Photovoltaics)")
    plt.xlabel("Month")
    plt.ylabel("Energy Generation (MWh)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_FOLDER, 'energy_by_type_stacked.png'))
    plt.close()

def plot_total_energy_line(df):
    plt.figure(figsize=(12, 6))
    plt.plot(df['month'], df['total_mwh'], marker='o', linestyle='-', color='blue', label='Total Energy Generation')
    plt.xticks(rotation=45)
    plt.title("Energy Generation Trends Over Time (2021)")
    plt.xlabel("Month")
    plt.ylabel("Energy Generation (MWh)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_FOLDER, 'total_energy_line.png'))
    plt.close()

def plot_individual_type_trends(df):
    plt.figure(figsize=(12, 6))
    plt.plot(df['month'], df['wind_offshore'], marker='o', label='Wind Offshore', color='green')
    plt.plot(df['month'], df['wind_onshore'], marker='s', label='Wind Onshore', linestyle='--', color='red')
    plt.plot(df['month'], df['photovoltaics'], marker='^', label='Photovoltaics', linestyle='-.', color='orange')
    plt.xticks(rotation=45)
    plt.title("Monthly Breakdown of Renewable Energy Contributions (2021)")
    plt.xlabel("Month")
    plt.ylabel("Energy Generation (MWh)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_FOLDER, 'individual_trends.png'))
    plt.close()

def plot_forecast(df):
    df = df.copy()
    df['month'] = pd.to_datetime(df['month'])
    df.set_index('month', inplace=True)

    # Use Holt-Winters with trend only (no seasonal)
    model = ExponentialSmoothing(df['total_mwh'], trend='add', seasonal=None)
    fit = model.fit()

    forecast = fit.forecast(12)
    forecast.index = pd.date_range(start=df.index[-1] + pd.offsets.MonthBegin(), periods=12, freq='MS')

    # Add synthetic sinusoidal seasonality
    seasonality = 0.05 * forecast.mean() * np.sin(np.linspace(0, 2 * np.pi, 12))
    forecast = forecast + seasonality

    # Combine actual and forecast
    full_series = pd.concat([df['total_mwh'], forecast])

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(full_series.index.strftime('%Y-%m'), full_series, marker='o', label='Forecast + Actual', color='navy')
    plt.axvline(df.index[-1].strftime('%Y-%m'), color='gray', linestyle='--', label='Forecast Start')
    plt.xticks(rotation=45)
    plt.title("Forecast with Synthetic Seasonality (Holt-Winters, Trend Only)")
    plt.xlabel("Month")
    plt.ylabel("Energy Generation (MWh)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_FOLDER, 'energy_forecast.png'))
    plt.close()

@app.route('/')
def index():
    df = fetch_monthly_data()
    plot_stacked_bar(df)
    plot_total_energy_line(df)
    plot_individual_type_trends(df)
    plot_forecast(df)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

