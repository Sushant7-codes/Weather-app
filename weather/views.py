from django.shortcuts import render
import json
import urllib.request
import urllib.error  # For handling HTTP errors

def index(request):
    city = ''
    data = {}

    if request.method == 'POST':
        city = request.POST['city']
        API_KEY = 'a8f521228c76c0d077db485a69b8b74d'  # <-- use this or the other key

        try:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
            res = urllib.request.urlopen(url).read()
            json_data = json.loads(res)

            # Convert temperature from Kelvin to Celsius
            temp_kelvin = json_data['main']['temp']
            temp_celsius = temp_kelvin - 273.15
            
            data = {
                "country_code": str(json_data['sys']['country']),
                "coordinate": str(json_data['coord']['lon']) + '°, ' + str(json_data['coord']['lat']) + '°',
                "temp": f"{temp_celsius:.1f}",  # Round to 1 decimal place
                "pressure": str(json_data['main']['pressure']),
                "humidity": str(json_data['main']['humidity']),
            }

        except urllib.error.HTTPError as e:
            data = {"error": f"HTTP Error {e.code}: {e.reason}"}
        except Exception as e:
            data = {"error": str(e)}
   
    return render(request, 'index.html', {'city': city, 'data': data})