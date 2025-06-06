#include "header.h"

void setup () {
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  WiFi.begin(hostname_esp, pass_esp, 6);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  String ip = WiFi.localIP().toString();
  Serial.println("\nWiFi connected");
  Serial.print("IP address: ");
  Serial.println(ip);

  Client.setServer(mqtt_server, mqtt_port);
  Client.setCallback(callback);
  Client.setKeepAlive(30);         // Ping server setiap 30 detik
  Client.setSocketTimeout(5);      // Timeout koneksi 5 detik

  dht.setup(DHTPIN, DHTesp::DHTTYPE);

  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    Serial.flush();
    while (1) delay(10);
  }

  if (! rtc.isrunning()) {
    Serial.println("RTC is NOT running, let's set the time!");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
}

void loop () {
  unsigned long current_time = millis();
  if(current_time-prev_time>input_rate){
    if (!Client.connected()) {
      if(current_time-prev_connect>connect_rate){
          reconnectMQTT();
          prev_connect = current_time;
      }
    }
    TempAndHumidity data = dht.getTempAndHumidity();
    temperature_val = data.temperature;
    humidity_val = data.humidity;
    String timestamp = getTimestamp();
    
    Client.loop();
    publishData(temperature_val, humidity_val, timestamp);
  }
}