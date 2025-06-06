'''
Writing rule :  variable, file name = snake_case
                constant = UPPER_CASE
                func/method = camelCase
                class = PascalCase
                string = double quote
                function gap = 2 blank line

3. Sampling data sensor dari web : https://openweathermap.org/current
    - Sampling berdasarkan input nama kota->ambil nilai "temp" dan "humidity" dari response API
    - Simpan data hasil sampling he json file dengan nama data_weather.json pada folder log
    - Print out program saat :
        Berhasil = (Timestamp GMT+7) - Success Running Sampling Data Weather with Result Temperature (Value Temperature) (Satuan Value Temperature) & Humidity (Value Humidity) (Satuan Value Humidity)
        Gagal = (Timestamp GMT+7) - Failed Running Sampling Data Weather with Status Code (Status Code) - (Return Message API)
    - Input = interval diatas 0 dalam satuan detik, print reminder message jika user bukan memasukan angka dan angka <= 0
    - Source code terdiri dari 2 file (main dan support file) dengan paradigma OOP
'''
import json, time, os
from datetime import datetime, timedelta
from soal3_function import WeatherSampler

api_key = "83b1a7b1aac758c61e46b963659a395e"

class ManageData():
    def __init__(self, api_key: str, city_name: str, sampling_period: float):
        self.api_key = api_key
        self.periode = sampling_period*1000
        self.city = city_name
        self.weather_data = None

        self.output_dir = "soal_python\log"
        self.output_file = os.path.join(self.output_dir, "data_weather.json")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)


    def runSampling(self)->None:
        sampler = WeatherSampler(api_key=self.api_key)
        prev_timing = 0
        while True:
            timestamp = datetime.now() + timedelta(hours=7)
            current_time = time.time_ns()/1000000 #convert to ms
            if (current_time-prev_timing)>self.periode:
                self.weather_data = sampler.getWeatherData(self.city)
                if self.weather_data['status'] == '200:Success':
                    print(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - Success Running Sampling Data Weather with Result "
                        f"Temperature {self.weather_data["message"]["temp"]} {self.weather_data["message"]["temp_unit"]} & Humidity {self.weather_data["message"]["humidity"]} {self.weather_data["message"]["humidity_unit"]}")
                    self._saveToJson(self.weather_data["message"])
                else:
                    print(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - Failed Running Sampling Data Weather with Status Code "
                        f"{self.weather_data["status"][:3]} - {self.weather_data["message"]}")

                prev_timing = current_time
    

    def _saveToJson(self, data: dict)->None:
        if os.path.exists(self.output_file):
            with open(self.output_file, 'r') as f:
                try:
                    all_data = json.load(f)
                except json.JSONDecodeError:
                    all_data = []
        else:
            all_data = []

        all_data.append(data)

        with open(self.output_file, 'w') as f:
            json.dump(all_data, f, indent=4)
            

def getSamplingInterval()->float:
    while True:
        sampling_interval = input("Input the sampling interval (in sec, > 0): ")
        try:
            interval = float(sampling_interval)
            if interval>0:
                return interval
            else:
                print("Interval must be above 0, try again ...")
        except ValueError:
            print("Invalid input, must be a number and above 0")


def getCityName()->str:
    return str(input("Name of the city : "))


def main():
    GetData = ManageData(api_key, "London", 1)
    GetData.runSampling()
    

if __name__=="__main__":
    main()