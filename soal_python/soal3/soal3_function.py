import requests
from datetime import datetime, timedelta

class WeatherSampler:
    def __init__(self, api_key: str):
        self.get_coord_url = "http://api.openweathermap.org/geo/1.0/direct"
        self.get_weather_url = "https://api.openweathermap.org/data/2.5/weather"
        self.api_key = api_key
        self.city_lon, self.city_lat = 0.0, 0.0

    
    def getWeatherData(self, city: str)->dict:
        status, msg = self.getCityCoord(city)
        if msg == "Success":
            params = {
                "lat": self.city_lat,
                "lon": self.city_lon,
                "appid": self.api_key,
                "units": "metric"
            }
            try:
                response = requests.get(url=self.get_weather_url, params=params)
                stat_val = response.status_code
                if stat_val == 200:
                    data = response.json()
                    
                    return {
                        "status": f"{stat_val}: Success",
                        "message": { "timestamp": (datetime.now() + timedelta(hours=7)).isoformat(),
                                    "temp": data["main"]["temp"],
                                    "temp_unit": "C",
                                    "humidity": data["main"]["humidity"],
                                    "humidity_unit": "%"}
                    }

                else:
                    return {
                        "status": f"{stat_val}: Failed to get weather data of the city",
                        "message": response.reason
                    }
    
            except Exception as e:
                return {
                        "status": "N/A: Failed to get weather data of the city",
                        "message": str(e)
                    }
        else:
            return {
                    "status": f"{status}: Failed to get lon and lat data of the city",
                    "message": msg
                }


    def getCityCoord(self, city: str)->tuple:
        params = {
            "q": city,
            "limit": 1,
            "appid": self.api_key,
        }
        try:
            response = requests.get(url=self.get_coord_url, params=params)
            stat = response.status_code
            if  stat == 200:
                city_lat_long = response.json()
                self.city_lat, self.city_lon = city_lat_long[0]["lat"], city_lat_long[0]["lon"]
                return stat, "Success"
               
            else:
                return stat, "Failed : Not get lon and lat of the city"

        except Exception as e:
            return 520, str(e)
                    