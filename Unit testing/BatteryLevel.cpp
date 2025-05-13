#include <Arduino.h>

#define ANALOG_PIN 34  

float actualVoltage;

const float VREF = 3.3;     // ESP32 reference voltage
const int ADC_RES = 4095;   // 12-bit resolution

const float R1 = 30000.0;   // 30kΩ
const float R2 = 10000.0;   // 10kΩ

void batteryVoltage(int adcValue) {
    float voltageAtPin = (adcValue * VREF) / ADC_RES;

    // Calculate actual voltage using the voltage divider formula:
    actualVoltage = voltageAtPin * ((R1 + R2) / R2);

    Serial.print("Battery Voltage: ");
    Serial.print(actualVoltage, 2);  // Print with 2 decimal places
    Serial.println(" V");
}

void setup() {
    Serial.begin(115200);
    analogReadResolution(12);        // Set 12-bit ADC resolution
    analogSetAttenuation(ADC_11db);  // Set full-scale input range (~3.3V)
}

void loop() {
    int adcValue = analogRead(ANALOG_PIN);
    batteryVoltage(adcValue);
    delay(1000);
}
