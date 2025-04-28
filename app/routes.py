from flask import Blueprint, render_template
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import os

main = Blueprint('main', __name__)

@main.route("/")
def index():
    conn = psycopg2.connect(
        host="metro.proxy.rlwy.net",
        port=36911,
        database="railway",
        user="postgres",
        password="LxbHTuXlGffdkdNGtwwMaOIvPkjAXYaE"
    )

    query = """
        SELECT timestamp, "Total[MWh]", "Wind offshore[MWh]", "Wind onshore[MWh]", "Photovoltaics[MWh]" 
        FROM energy_generation
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    os.makedirs("app/static", exist_ok=True)

    # 1. Total Energy Generation Yearly
    df['Total[MWh]'].resample('M').sum().plot(title="Monthly Total Energy Generation")
    plt.ylabel("MWh")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("app/static/total_generation.png")
    plt.clf()

    # 2. Generation by Type
    df[['Wind offshore[MWh]', 'Wind onshore[MWh]', 'Photovoltaics[MWh]']].resample('M').sum().plot(
        title="Monthly Energy Generation by Type"
    )
    plt.ylabel("MWh")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("app/static/by_type.png")
    plt.clf()

    # 3. Trends Over Time
    df.resample('W').mean().plot(title="Weekly Average Energy Trends")
    plt.ylabel("MWh")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("app/static/trends.png")
    plt.clf()

    return render_template("index.html")
