#include <Wire.h>

int thermBeta = 3950;
int thermResistance = 10;
// analog inputs
int thermistorPin = 0; 
int soilMoisturePin = 1;
int lightSensorPin = 2;

void setup() {//  Serial.print("Temperature in Kelvin: "+String(kTemp)+"\n");

  Serial.begin(9600);
  // put your setup code here, to run once:
}

void loop() {
  delay(1000);
  Serial.println();
  long thermVal = 1023 - analogRead(thermistorPin);
  long soilVal = analogRead(soilMoisturePin);
  long lightVal = analogRead(lightSensorPin);
  String tempOutput = getTempReadings(thermVal);
  String soilOutput = "\"soil_moisture\" : "+String(soilVal)+", ";
  String lightOutput = "\"light_level\" : "+String(normalizeLightVal(lightVal))+" }";
  String json = tempOutput+soilOutput+lightOutput;
  Serial.println(json);
}

String getTempReadings(long thermVal) {
      float cTemp = getTempC(thermVal);
      float fTemp = getTempF(cTemp);
      float kTemp = getTempK(fTemp);
      return "{ \"temperature\" : { \"c\":"+String(cTemp)+", \"f\":"+String(fTemp)+", \"k\":"+String(kTemp)+" }, ";
}

float normalizeLightVal(long lightVal) {
  return 1025 - lightVal;  
}

float getTempC(long rawVal) {
  return thermBeta /(log((1025.0 * 10 / rawVal - 10) / 10) + thermBeta / 298.0) - 273.0;
}

float getTempF(float tempC) {
  return 1.8 * tempC + 32.0;
}

float getTempK(float tempF) {
  return (((tempF - 32) * 5) / 9) + 273.15;
}
