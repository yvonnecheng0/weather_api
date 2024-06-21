import requests
import pandas as pd
import sqlalchemy as db

api_key = 'e9ade545133ca72b0db7d4ba4ef4200c'
city = 'London'
base_url = 'http://api.openweathermap.org/data/2.5/weather'
url = f'{base_url}?q={city}&appid={api_key}&units=metric'

response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    data = response.json()
    weather_data = {
        'City': [data['name']],
        'Temperature': [data['main']['temp']],
        'Weather': [data['weather'][0]['description']]
    }
else:
    print("Failed to retrieve data.")

# Convert dict into DataFrame
df = pd.DataFrame.from_dict(weather_data)
print(df)

# Create engine object
engine = db.create_engine('sqlite:///weather_data.db')

# Create and send SQL table from DataFrame
df.to_sql('weather', con=engine, if_exists='replace', index=False)

# Write query and print out requests
with engine.connect() as connection:
    results = connection.execute(db.text("SELECT * FROM weather;")).fetchall()
    print(pd.DataFrame(results, columns=['City', 'Temperature', 'Weather']))
