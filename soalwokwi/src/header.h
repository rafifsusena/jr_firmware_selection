/* ==== LIBRARY === */
#include <WiFi.h>
#include <WiFiClient.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

#include "RTClib.h"
#include "DHTesp.h"

#define DHTPIN 18
#define DHTTYPE DHT22

/* --- OBJECT --- */
WiFiClient EspClient;
PubSubClient Client(EspClient);
JsonDocument Data;
RTC_DS1307 rtc;
DHTesp dht;

/* --- CONNECTION CREDENTIAL ---*/
const char* hostname_esp = "Wokwi-GUEST";
const char* pass_esp = "";

// MQTT server
const char* mqtt_server = "test.mosquitto.org";
const int mqtt_port = 1883;
String mqtt_topic = "mqtt/rafif/data ";
String name = "rafif";

//Timing
unsigned long current_time, prev_time, prevTime, prev_connect = 0;
const int input_rate = 10;
const int publish_period = 5000;
const int connect_rate = 2500;

float humidity_val, temperature_val = 0;

String getTimestamp(){
  DateTime now = rtc.now();

  String yearStr = String(now.year(), DEC);
  String monthStr = (now.month() < 10 ? "0" : "") + String(now.month(), DEC);
  String dayStr = (now.day() < 10 ? "0" : "") + String(now.day(), DEC);
  String hourStr = (now.hour() < 10 ? "0" : "") + String(now.hour(), DEC); 
  String minuteStr = (now.minute() < 10 ? "0" : "") + String(now.minute(), DEC);
  String secondStr = (now.second() < 10 ? "0" : "") + String(now.second(), DEC);

  // Complete time string
  return (yearStr + "-" + monthStr + "-" + dayStr + " " + hourStr + ":" + minuteStr + ":" + secondStr);

}

void publishData(float temp, float hum, String timestamp) {
  unsigned long currentTime = millis();
  if (currentTime - prevTime >= publish_period) {
    Data["nama"] = name;
    Data["data"]["temperature"]   = temp;
    Data["data"]["humidity"] = hum;
    Data["timestamp"] = timestamp;
    String payload;
    serializeJson(Data, payload);
    bool success = Client.publish(mqtt_topic.c_str(), payload.c_str());
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
    prevTime = currentTime;
  }
}

//Reconnect to MQTT server
void reconnectMQTT() {
  unsigned long startAttemptTime = millis();
  if (!Client.connected()) { 
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