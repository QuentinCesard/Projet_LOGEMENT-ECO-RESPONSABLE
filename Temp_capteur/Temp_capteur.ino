/**
   PostHTTPClient.ino

    Created on: 21.11.2016

*/
#include "DHT.h"
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

/* this can be run with an emulated server on host:
        cd esp8266-core-root-dir
        cd tests/host
        make ../../libraries/ESP8266WebServer/examples/PostServer/PostServer
        bin/PostServer/PostServer
   then put your PC's IP address in SERVER_IP below, port 9080 (instead of default 80):
*/
//#define SERVER_IP "10.0.1.7:9080" // PC address with emulation on host
#define SERVER_IP "192.168.1.16:8000"
#define DHTPIN 14 
#define DHTTYPE DHT22 

#ifndef STASSID
#define STASSID "Livebox-9F36"
#define STAPSK "aPXeTAcmpsp7HzWPZC"
#endif

#define ID_capteur 2

DHT dht(DHTPIN, DHTTYPE);  // Initialisation du capteur DHT

void setup() {

  Serial.begin(9600);

  Serial.println();
  Serial.println();
  Serial.println();
  dht.begin();  // Démarrage du capteur DHT
  WiFi.begin(STASSID, STAPSK);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  // wait for WiFi connection
  if ((WiFi.status() == WL_CONNECTED)) {

    WiFiClient client;
    HTTPClient http;

    Serial.print("[HTTP] begin...\n");
    // configure traged server and url
    http.begin(client, "http://" SERVER_IP "/postplain/");  // HTTP
    http.addHeader("Content-Type", "application/json");

    String postData = "{\"id\": \"" + String(ID_capteur) + "\" , \"temperature\": \"" + String(t) + "\", \"humidity\": \"" + String(h) + "\"}";
    Serial.print("[HTTP] POST...  ");
    Serial.println(postData);
    // start connection and send HTTP header and body

    int httpCode = http.POST(postData);

    // httpCode will be negative on error
    if (httpCode > 0) {
      // HTTP header has been send and Server response header has been handled
      Serial.printf("[HTTP] POST... code: %d\n", httpCode);

      // file found at server
      if (httpCode == HTTP_CODE_OK) {
        const String& payload = http.getString();
        Serial.println("received payload:\n<<");
        Serial.println(payload);
        Serial.println(">>");
      }
    }else{
      Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
  }

