import requests
import pandas as pd
import json

def fetch_opensky_batch():
    
    url = "https://opensky-network.org/api/states/all"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        states = data.get('states', [])
        columns = [
            'icao24', 'callsign', 'origin_country', 'time_position', 
            'last_contact', 'longitude', 'latitude', 'baro_altitude', 
            'on_ground', 'velocity', 'true_track', 'vertical_rate', 
            'sensors', 'geo_altitude', 'squawk', 'spi', 'position_source'
        ]
        
        df = pd.DataFrame(states, columns=columns)
        df['callsign'] = df['callsign'].str.strip()
        df_airborne = df[(df['on_ground'] == False) & (df['longitude'].notna()) & (df['latitude'].notna())]
        
        
        df_airborne['transit_status'] = df_airborne['velocity'].apply(
            lambda v: 'Delayed / Bottleneck' if (v and v < 200) else 'On-Time / Optimal'
        )
        
        df_airborne['asset_efficiency_score'] = (df_airborne['baro_altitude'] / (df_airborne['velocity'] + 1)).round(2)
        
        output_file = "live_transit_fleet_batch.csv"
        df_airborne.to_csv(output_file, index=False)
        print(f"{len(df_airborne)}")
        print(f"Saved file to: {output_file}")
        
    else:
        print(f"Server status code: {response.status_code}")

if __name__ == "__main__":
    fetch_opensky_batch()
