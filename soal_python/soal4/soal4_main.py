'''
Writing rule :  variable, file name = snake_case
                constant = UPPER_CASE
                func/method = camelCase
                class = PascalCase
                string = double quote
                function gap = 2 blank line

4. Buat program dengan konsep OOP dengan 1 file main dan file fungsi pendukung untuk :
    - Kirim data json ker server mosquitto.org dengan topik=mqtt/(nama kandidat)/data
    - Format data : 
    {
        "nama": "(nama)",
        "data":
            "sensor1": "(value random 0 - 100)", 
            "sensor1": "(value random 0 - 1000)", 
            "sensor1": "(value random true/false)", 
            "sensor1": "(value temperature)", #Diambil dari json file no.3
            "sensor1": "(value humidity)" #Diambil dari json file no.3
        },
        "timestamp": "(timestamp format UTC yyyy-mm-dd HH:MM:SS)"
    }
    - Interval 5 detik, catat log kirim data pada csv file pada folder log: mqtt_log_(tanggal bulan tahun).csv 
    - Log format : timestamp;sensor1;sensor2;sensor3;sensor4;sensor5;sensor6;status
    - Print out saat publish data : 
        Timestamp : (Timestamp dengan format waktu GMT+7 yyyy-mm-dd HH:MM:SS)
        Action : Publish
        Topic : (Topic)
        Data : (Data Pack JSON yang dikirim ke MQTT)
        State : (Success/Failed)
'''
import time, json, csv, os
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta
from soal4_function import GetData

NAMA_KANDIDAT = "rafif"

class DataPublisher:
    def __init__(self, name: str):
        self.name = name.lower()

        #MQTT
        self.topic = f"mqtt/{self.name}/data"
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.onConnect
        self.client.connect_async(host="test.mosquitto.org")
        self.client.loop_start() #Network loop non-blocking
        
        #Log directory
        self.log_dir = "log"
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        #Data handling
        self.data = GetData(self.name, os.path.join(self.log_dir, "data_weather.json"))

    
    def _logToCsv(self, timestamp_gmt7: str, sensor: list, status: str):
            filename = f"mqtt_log_{datetime.now().strftime('%d%m%y')}.csv"
            filepath = os.path.join(self.log_dir, filename)
            write_header = not os.path.exists(filepath)
            with open(filepath, mode="a", newline="") as file:
                writer = csv.writer(file, delimiter=';')
                if write_header:
                    writer.writerow(["timestamp", "sensor1", "sensor2", "sensor3", "sensor4", "sensor5", "status"])
                writer.writerow([
                    str(timestamp_gmt7), sensor[0], sensor[1], sensor[2], sensor[3], sensor[4], status
                ])

    
    def onConnect(self, client, userdata, flags, reason_code, properties)->None:
        print(f"Connected with result code {reason_code}")

    
    def pubLoop(self)->None:
        #Timing
        interval = 5
        prev_time = 0
        while True:
            current_time = time.time()
            if (current_time-prev_time) > interval:
                self.data.getData()
                sensor = self.data.sensor
                payload = self.data.getPayload()
                json_payload = json.dumps(payload)
                timestamp_gmt7 = (datetime.now() + timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S")
                try:
                    result = self.client.publish(self.topic, json_payload)
                    status = "Success" if result.rc == mqtt.MQTT_ERR_SUCCESS else "Failed"
                except:
                    status = "Failed"
                
                self._logToCsv(timestamp_gmt7, sensor, status)

                print(f"Timestamp : {timestamp_gmt7}")
                print(f"Action : Publish")
                print(f"Topic : {self.topic}")
                print(f"Data : {json_payload}")
                print(f"State : {status}\n")
                
                prev_time = current_time


def main()->None:
    name = input("Masukkan nama kandidat (satu kata, tanpa spasi): ").strip()
    if " " in name or not name:
        print("Nama kandidat harus satu kata tanpa spasi dan tidak boleh kosong.")
        return
    
    Publisher = DataPublisher(name=name)
    Publisher.pubLoop()

if __name__ == "__main__":
    main()

