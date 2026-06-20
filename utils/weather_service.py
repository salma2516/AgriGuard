import requests

API_KEY ="YOUR_WEATHER_API_KEY"

def get_weather(city):

    try:

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url)

        print("Response:")
        print(response.text)

        data = response.json()

        if "name" not in data:

            print("API Error:", data)

            return None

        return {

            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]

        }

    except Exception as e:

        print("Weather Error:", e)

        return None