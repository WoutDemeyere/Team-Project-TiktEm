// stuff voor de LED
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

const int PIN = 15;
const int NUMPIXELS = 1;

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  pixels.begin();
}

void loop() {
  pixels.clear();
  pixels.setBrightness(10);
  pixels.setPixelColor(0, pixels.Color(0, 255, 0));
  pixels.show();
}
