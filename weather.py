import requests
import pandas as pd
import sqlalchemy as db

def fetch_weather_data(api_key, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return {
            'City': data['name'],
            'Temperature': data['main']['temp'],
            'Weather': data['weather'][0]['description']
        }
    else:
        raise Exception("Failed to retrieve data")

def convert_to_dataframe(weather_data):
    return pd.DataFrame([weather_data])

def save_to_database(df, db_name, table_name):
    engine = db.create_engine(f'sqlite:///{db_name}.db')
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    return engine

def query_database(engine, table_name):
    with engine.connect() as connection:
        results = connection.execute(db.text(f"SELECT * FROM {table_name};")).fetchall()
        return pd.DataFrame(results, columns=['City', 'Temperature', 'Weather'])

if __name__ == "__main__":
    api_key = 'e9ade545133ca72b0db7d4ba4ef4200c'
    city = 'London'
    
    weather_data = fetch_weather_data(api_key, city)
    df = convert_to_dataframe(weather_data)
    engine = save_to_database(df, 'weather_data', 'weather')
    result_df = query_database(engine, 'weather')
    print(result_df)
