#include <Arduino.h>
#include <Wire.h>

float RateRoll, RatePitch, RateYaw;

void gyro_signals(){
    //switch on low pass filter
    Wire.beginTransmission(0x68); 
    Wire.write(0x1A);
    Wire.write(0x05);
    Wire.endTransmission();

    //set sensitivity scale factor
    Wire.beginTransmission(0x68); 
    Wire.write(0x1B);
    Wire.write(0x8);
    Wire.endTransmission();

    //access gyro measurements
    Wire.beginTransmission(0x68); 
    Wire.write(0x43);
    Wire.endTransmission();
    Wire.requestFrom(0x68,6)

    //read the gyro measurements around each axis
    int16_t GyroX=Wire.read()<<8 | Wire.read();
    int16_t GyroY=Wire.read()<<8 | Wire.read();
    int16_t GyroZ=Wire.read()<<8 | Wire.read();

    //convert the measurements into degrees per second
    RateRoll=(float)GyroX/65.5;
    RatePitch=(float)GyroY/65.5;
    RateYaw=(float)GyroZ/65.5;
}

void setup() {
  Serial.begin(57600);
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
  Wire.setClock(400000);
  Wire.begin();
  delay(250);

  //start the gyro in power mode
  Wire.beginTransmission(0x68); 
  Wire.write(0x6B);
  Wire.write(0x00);
  Wire.endTransmission();
}

void loop() {
  gyro_signals();
  Serial.print("Roll rate [°/s]= ");
  Serial.print(RateRoll);
  Serial.print(" Pitch Rate [°/s]= ");
  Serial.print(RatePitch);
  Serial.print(" Yaw Rate [°/s]= ");
  Serial.println(RateYaw);
  delay(50);
}