#include <Arduino.h>
#include <WiFi.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>

#include "config.hpp"
#include "dac_output.hpp"
#include "control_state.hpp"
//----------------------------------------------------
// Global Objects
//----------------------------------------------------

WebSocketsClient webSocket;

// ArduinoJson v7
JsonDocument json;

//----------------------------------------------------
// Control State
//----------------------------------------------------
ControlState state;

//----------------------------------------------------
// WiFi
//----------------------------------------------------

void connectWiFi()
{
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

Serial.print("Connecting to ");
Serial.println(WIFI_SSID);

uint8_t attempts = 0;

while (WiFi.status() != WL_CONNECTED)
{
    delay(500);

    Serial.print(".");

    attempts++;

    if (attempts >= 40)
    {
        Serial.println();
        Serial.println("Connection Timeout");

        Serial.print("WiFi Status = ");
        Serial.println(WiFi.status());

        break;
    }
}

if (WiFi.status() == WL_CONNECTED)
{
    Serial.println();
    Serial.println("WiFi Connected!");

    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
}
}


//----------------------------------------------------
// WebSocket Callback
//----------------------------------------------------

void webSocketEvent(
    WStype_t type,
    uint8_t *payload,
    size_t length)
{
    switch (type)
    {
        case WStype_CONNECTED:
        {
            Serial.println("Connected to WebSocket Server");
            break;
        }

        case WStype_DISCONNECTED:
        {
            Serial.println("Disconnected from Server");
            break;
        }

        case WStype_TEXT:
        {

            DeserializationError err = deserializeJson(json, payload, length);

            if (err)
            {
                Serial.print("JSON Parse Error: ");
                Serial.println(err.c_str());
                break;
            }
            
            state.timestamp = json["timestamp"];
            state.roll = json["roll"];
            state.pitch = json["pitch"];
            state.yaw = json["yaw"];
            state.throttle = json["throttle"];

            updateDAC(state);

            break;
        }

        default:
        {
            break;
        }
    }
}

//----------------------------------------------------
// Setup
//----------------------------------------------------

void setup()
{
    Serial.begin(115200);

    delay(1000);

    connectWiFi();

    initDAC();

    webSocket.begin(
        WS_HOST,
        WS_PORT,
        "/"
    );

    webSocket.onEvent(webSocketEvent);

    webSocket.setReconnectInterval(5000);
}

//----------------------------------------------------
// Loop
//----------------------------------------------------

void loop()
{
    //for safety, if we don't receive a packet for 250 ms, we will set all values to 0
    static unsigned long lastPacketTime = millis();
    if (millis() - lastPacketTime > 250)
    {
        // No packet for 250 ms

        state.roll = 0;
        state.pitch = 0;
        state.yaw = 0;
        state.throttle = 0;

        updateDAC(state);
    }
    lastPacketTime = millis();


    webSocket.loop();

}