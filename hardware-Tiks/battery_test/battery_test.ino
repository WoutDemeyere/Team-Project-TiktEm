#include <Adafruit_NeoPixel.h>

const int batteryPin = 25;
const int batteryMin = 2480;
int batteryPercent = 0;

/* LED  */
const int LED_PIN = 15;
const int NUMPIXELS = 1;
Adafruit_NeoPixel pixels(NUMPIXELS, LED_PIN, NEO_RGB + NEO_KHZ800);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  readBattery();
}

void led_on(int r, int g, int b) {
  pixels.clear();
  pixels.setBrightness(255);
  pixels.setPixelColor(0, pixels.Color(r, g, b));
  pixels.show();
}

void readBattery(){
  int batteryValue = analogRead(batteryPin);  
  batteryValue -= batteryMin;
  batteryPercent = batteryValue / 9.75;
  if (batteryPercent >= 100){
    batteryPercent = 100;
  }
  else if (batteryPercent <= 0){
    batteryPercent = 0;
  }
  Serial.println(batteryPercent);
  
  int green = batteryPercent * 2.55;
  int red = 255 - green;
  led_on(red, green, 0);
  delay(50);
}
