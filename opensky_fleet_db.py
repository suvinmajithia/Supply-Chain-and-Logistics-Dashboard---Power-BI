import sqlite3
import json
import pandas as pd

print("Reading your local JSON flight data...")

# 1. Open your local desktop JSON file instead of making a web call
with open("opensky_raw_cache.json", "r") as f:
    raw_flights = json.load(f)

columns = [
    'icao24', 'callsign', 'origin_country', 'time_position', 
    'last_contact', 'longitude', 'latitude', 'baro_altitude', 
    'on_ground', 'velocity', 'true_track', 'vertical_rate', 
    'sensors', 'geo_altitude', 'squawk', 'spi', 'position_source'
]
df = pd.DataFrame(raw_flights, columns=columns)

# 2. Clean up the rows
df = df.dropna(subset=['latitude', 'longitude'])
df['icao24'] = df['icao24'].astype(str)
df['callsign'] = df['callsign'].astype(str).str.strip()
df['origin_country'] = df['origin_country'].astype(str)

# 3. Add your 1, 2, 3 row index right at the front
df.insert(0, 'index_id', range(1, len(df) + 1))

# 4. Save directly into your SQL database file
connection = sqlite3.connect("fleet_warehouse.db")
df.to_sql("active_fleet_table", connection, if_exists="replace", index=False)
connection.close()

print("Your local data is now stored inside the 'fleet_warehouse.db' SQL table.")
