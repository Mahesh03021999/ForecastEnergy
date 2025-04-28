# main.py
import pandas as pd

def load_energy_data(file_path):
    df = pd.read_excel(file_path, skiprows=6)

    df.replace('-', pd.NA, inplace=True)
    numeric_cols = ['Total[MWh]', 'Wind offshore[MWh]', 'Wind onshore[MWh]', 'Photovoltaics[MWh]', 'Other[MWh]']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    df['timestamp'] = pd.to_datetime(df['Date'] + ' ' + df['Time of day'], errors='coerce')
    df.dropna(subset=['timestamp'], inplace=True)

    return df[['timestamp'] + numeric_cols]
