/* ==== LIBRARY === */
#include <WiFi.h>
#include <WiFiClient.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <freertos/semphr.h>

#include "RTClib.h"
#include "DHTesp.h"

#define DHTPIN 18
#define DHTTYPE DHT22

/* --- OBJECT --- */
WiFiClient EspClient;
PubSubClient Client(EspClient);
JsonDocument Data;
RTC_DS1307 Rtc;
DHTesp Dht;

/* --- CONNECTION CREDENTIAL ---*/
const char* hostname_esp = "Wokwi-GUEST";
const char* pass_esp = "";

// MQTT server
const char* mqtt_server = "test.mosquitto.org";
const int mqtt_port = 1883;
String mqtt_topic = "mqtt/rafif/data ";
String name = "rafif";

//Timing
unsigned long current_time, prev_time, prev_read_time, prev_connect = 0;
const int input_rate = 10;
const int publish_rate = 5000;
const int connect_rate = 100;

// Task periods
const TickType_t SENSOR_TASK_PERIOD = pdMS_TO_TICKS(5);   // 0.5 ms
const TickType_t PUBSUB_TASK_PERIOD = pdMS_TO_TICKS(10);  // 1 second
SemaphoreHandle_t dataMutex;

float humidity_val, temperature_val = 0;
String timestamp = "";

/* --- FUNCTION/PROCEDURE --- */
void readSensorTask(void* pvParameters);
void pubSubTask(void* pvParameters);
String getTimestamp();
void publishData(float temp, float hum, String timestamp, unsigned long publish_start_us);
void reconnectMQTT();
void callback(char* topic, byte* payload, unsigned int length);