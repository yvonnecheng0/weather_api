import requests

api_key = 'e9ade545133ca72b0db7d4ba4ef4200c'

city = 'London'

url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

response = requests.get(url)

#Check if request was successful
if response.status_code == 200:
  data = response.json()
  city = data['name']
  temp = data['main']['temp']
  weather_descrp = data['weather'][0]['description']
  print(f"City: {city}")
  print(f"Temperatures:{temp}")
  print(f"Weather: {weather_descrp}")
else:
  print("Failed to retrieve data.")
  