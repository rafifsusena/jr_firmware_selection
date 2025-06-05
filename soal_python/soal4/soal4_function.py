import os, json, random
from datetime import datetime, timedelta

class GetData:
    def __init__(self, name: str, log_dir: str):
        self.name = name
        self.log_dir = log_dir

        self.sensor = [0,0,0,0,0]


    def getData(self)->None:
        self.sensor[0] = random.randint(0, 100)
        self.sensor[1] = round(random.uniform(0, 1000), 2)
        self.sensor[2] = random.choice([True, False])
        self.sensor[3], self.sensor[4] = self._readRecordFile(self.log_dir)
    

    def getPayload(self)->dict:
        timestamp_utc = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload = {
            "nama": self.name,
            "data": {
                "sensor1": self.sensor[0],
                "sensor2": self.sensor[1],
                "sensor3": self.sensor[2],
                "sensor4": self.sensor[3],
                "sensor5": self.sensor[4]
            },
            "timestamp": timestamp_utc
        }
        return payload

    
    def _readRecordFile(self, directory: str)->tuple:
        try:
            with open(directory, "r") as f:
                data = json.load(f)
                return data[-1]["temp"], data[-1]["humidity"]

        except Exception as e:
            print(f"{e} | {self.log_dir}")
            return 0.0, 0.0