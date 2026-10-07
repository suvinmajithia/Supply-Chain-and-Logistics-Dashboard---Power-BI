import os
import json
import requests
import pandas as pd

url = "https://opensky-network.org/api/states/all"
filename = "live_transit_fleet_batch.csv"
cache_file = "opensky_raw_cache.json"

try:
    response = requests.get(url, timeout=10)
    
    if response.status_code != 200:
        print(f"Server Busy - (Code {response.status_code}).")
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                raw_flights = json.load(f)
        else:
            raise Exception("No backup cache.")
    else:
        
        data = response.json()
        raw_flights = data.get('states', [])
        with open(cache_file, 'w') as f:
            json.dump(raw_flights, f)
       

    columns = [
        'icao24', 'callsign', 'origin_country', 'time_position', 
        'last_contact', 'longitude', 'latitude', 'baro_altitude', 
        'on_ground', 'velocity', 'true_track', 'vertical_rate', 
        'sensors', 'geo_altitude', 'squawk', 'spi', 'position_source'
    ]
    
    df = pd.DataFrame(raw_flights, columns=columns)
    
    # Drop rows that don't have location coordinates
    df = df.dropna(subset=['latitude', 'longitude'])
    
    # Clean up text codes and format as strings
    df['icao24'] = df['icao24'].astype(str)
    df['callsign'] = df['callsign'].astype(str).str.strip()
    df['origin_country'] = df['origin_country'].astype(str)
    df.insert(0, 'index_id', range(1, len(df) + 1))
    
    df.to_csv(filename, index=False)

except Exception as e:
    print(f"Error: {e}")
