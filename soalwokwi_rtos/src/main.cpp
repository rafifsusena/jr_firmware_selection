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

  Dht.setup(DHTPIN, DHTesp::DHTTYPE);

  if (! Rtc.begin()) {
    Serial.println("Couldn't find RTC");
    Serial.flush();
    while (1) delay(10);
  }

  if (! Rtc.isrunning()) {
    Serial.println("RTC is NOT running, let's set the time!");
    Rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
  delay(1000);

  // Initialize mutex
  dataMutex = xSemaphoreCreateMutex();
  if (dataMutex == NULL) {
    Serial.println("Failed to create mutex");
    while (1);
  }
  xTaskCreatePinnedToCore(readSensorTask, "Read Sensor Task", 2048, NULL, 3, NULL, 1); // Higher priority, Core 1
  xTaskCreatePinnedToCore(pubSubTask, "Pub-Sub Task", 4096, NULL, 1, NULL, 1);  // Lower priority, Core 1
}


void readSensorTask(void* pvParameters) {
  float temp_val = 0.0, hum_val = 0.0;
  const uint8_t max_fail_count = 3;
  uint8_t fail_count = 0;
  for (;;) {
    unsigned long current_time = millis();
    if ((long)(current_time - prev_read_time) >= input_rate) {
      TempAndHumidity data = Dht.getTempAndHumidity();

      if (!isnan(data.temperature) && !isnan(data.humidity)) {
        temp_val = data.temperature;
        hum_val = data.humidity;
        fail_count = 0;  // reset fail counter
      } else {
        Serial.println("[WARN] Failed to read from DHT sensor");
        fail_count++;
        if (fail_count >= max_fail_count) {
          Serial.println("[ERROR] DHT read failed multiple times. Check sensor connection.");
          fail_count = 0;  // reset again to avoid spam
        }
      }

      // Ambil timestamp dari RTC
      String date_time = getTimestamp();

      // Update nilai bersama dengan mutex
      if (xSemaphoreTake(dataMutex, portMAX_DELAY)) {
        temperature_val = temp_val;
        humidity_val = hum_val;
        timestamp = date_time;
        xSemaphoreGive(dataMutex);
      }

      prev_read_time = current_time;
    }

    // Minimal delay untuk menghindari watchdog
    vTaskDelay(10 / portTICK_PERIOD_MS);
  }
}


void pubSubTask(void* pvParameters) {
  float temp = 0.0, hum = 0.0;
  String timing = "";
  const TickType_t delay_tick = 10 / portTICK_PERIOD_MS;

  unsigned long last_publish_millis = millis();

  for (;;) {
    unsigned long now = millis();

    // Jaga koneksi MQTT
    if ((long)(now - prev_connect) >= connect_rate) {
      if (!Client.connected()) {
        reconnectMQTT();
      }
      prev_connect = now;
    }

    if (Client.connected()) {
      Client.loop();
    }

    // Publish tiap 5 detik dengan koreksi drift
    if ((long)(now - prev_time) >= publish_rate) {
      unsigned long actual_delay = now - prev_time;

      if (actual_delay > publish_rate + 1000) {
        Serial.print("[WARN] Publish delay lebih dari 1 detik! Delay: ");
        Serial.print(actual_delay);
        Serial.println(" ms");
      }

      prev_time += publish_rate; // Koreksi waktu publish agar tetap periodik

      // Ambil data sensor dari mutex
      if (xSemaphoreTake(dataMutex, portMAX_DELAY)) {
        temp = temperature_val;
        hum = humidity_val;
        timing = timestamp;
        xSemaphoreGive(dataMutex);
      }

      // Waktu aktual publish
      unsigned long publish_start_us = esp_timer_get_time();  // waktu dalam mikrodetik
      publishData(temp, hum, timing, publish_start_us);
    }

    vTaskDelay(delay_tick);
  }
}


void loop () {

}


String getTimestamp(){
  DateTime now = Rtc.now();

  String yearStr = String(now.year(), DEC);
  String monthStr = (now.month() < 10 ? "0" : "") + String(now.month(), DEC);
  String dayStr = (now.day() < 10 ? "0" : "") + String(now.day(), DEC);
  String hourStr = (now.hour() < 10 ? "0" : "") + String(now.hour(), DEC); 
  String minuteStr = (now.minute() < 10 ? "0" : "") + String(now.minute(), DEC);
  String secondStr = (now.second() < 10 ? "0" : "") + String(now.second(), DEC);

  // Complete time string
  return (yearStr + "-" + monthStr + "-" + dayStr + " " + hourStr + ":" + minuteStr + ":" + secondStr);

}


void publishData(float temp, float hum, String timestamp, unsigned long publish_start_us) {
  // Menyiapkan data JSON
  Data["nama"] = name;
  Data["data"]["temperature"] = temp;
  Data["data"]["humidity"] = hum;
  Data["timestamp"] = timestamp;
  
  // Konversi ke string JSON
  String payload;
  serializeJson(Data, payload);

  // Coba publish
  bool success = Client.publish(mqtt_topic.c_str(), payload.c_str());
  unsigned long publish_end_us = esp_timer_get_time();
  unsigned long elapsed_us = publish_end_us - publish_start_us;

  // Logging detail waktu
  Serial.println("=========================================");
  Serial.print("Datetime       : ");
  Serial.println(timestamp);  // Sudah dalam format GMT+7 jika RTC-nya diatur sesuai
  Serial.print("Temperature    : ");
  Serial.print(temp);
  Serial.println(" °C");
  Serial.print("Humidity       : ");
  Serial.print(hum);
  Serial.println(" %");
  Serial.print("Data Pack      : ");
  Serial.println(payload);
  Serial.print("Result Publish : ");
  Serial.println(success ? "Success" : "Failed");

  Serial.println("=========================================");
  Serial.println();
  if (!success) {
    Serial.println("[ERROR] MQTT publish failed. Cek koneksi atau broker.");
  }
  Serial.print("Publish Time   : ");
  Serial.print(elapsed_us / 1000.0, 3);
  Serial.println(" ms");
}


//Reconnect to MQTT server
void reconnectMQTT() {
  Serial.println("Attempting MQTT connection...");
  String clientId = "ESP32Client-" + String(random(0xffff), HEX);

  if (Client.connect(clientId.c_str())) {
    Serial.println("MQTT Connected");
  } else {
    Serial.print("failed, rc=");
    Serial.print(Client.state());
    Serial.println(" try again...");
  }
}


void callback(char* topic, byte* payload, unsigned int length){
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  String message = "";
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println(message);
}