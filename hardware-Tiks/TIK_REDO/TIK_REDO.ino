/* IMPORTS  */

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

/* TIK-ELEMENTS */
int TIK_ID = 0;

String TIK_HOSTNAME = "Tiktem-Tik" + String(TIK_ID);
String TIK_SUBTOPIC = "tiktem/tik" + String(TIK_ID);
char TIK_HOSTNAME_ARR[20];
char TIK_SUBTOPIC_ARR[20];
  
char* TIK_PUBTOPIC = "tiktem/tiksout";

boolean light_status = false;
boolean tik_status = false;

/* WIFI  */
const String used_wifi = "home-wout"; //"hotspot-wout", "howest-iot", "home-wout"

char* ssid = "";
char* password = "";
//char* ssid = "bosstraat";
//char* password =  "wotikrko22";

WiFiClient espClient;

/* MQTT  */
const char* mqttServer = "192.168.0.112";
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = "";

char raw_buffer[200];

PubSubClient client(espClient);

/* LED  */
const int LED_PIN = 15;
const int NUMPIXELS = 1;
Adafruit_NeoPixel pixels(NUMPIXELS, LED_PIN, NEO_RGB + NEO_KHZ800);

int red = 0;
int green = 0;
int blue = 0;

int brightness = 10;

/* BUZZER  */
int freq;
int channel = 0;
int resolution = 8;
const int buzzerPin = 26;
const int touchPin = 4;
int Tone = 0;

/* TOUCH  */
int touchWaardeHuidig;
int touchChangeCount = 0;
bool touchActive = false;
int touchInActiveCount = 0;
int touchGemiddelde = 0;
int touchTreshold = 10;

void led_on(int r, int g, int b) {
  pixels.clear();
  pixels.setBrightness(brightness);
  pixels.setPixelColor(0, pixels.Color(r, g, b));
  pixels.show();
}

void led_of() {
  pixels.clear();
  pixels.setBrightness(0);
  pixels.setPixelColor(0, pixels.Color(0, 0, 0));
  pixels.show();
}

void buzzer(int buzz) {
  ledcWriteTone(channel, buzz);
  delay(350);
  ledcWriteTone(channel, 0);
}

void setup_buzzer() {
  ledcSetup(channel, freq, resolution);
  ledcAttachPin(buzzerPin, channel);
  ledcWrite(channel, 127);
  ledcWriteTone(channel, 0);
}

void setup_wifi() {

  Serial.print("Selecting network ");
  Serial.println(used_wifi);
  
  TIK_HOSTNAME.toCharArray(TIK_HOSTNAME_ARR, 20);
  TIK_SUBTOPIC.toCharArray(TIK_SUBTOPIC_ARR, 20);

  if(used_wifi.equals("hotspot-wout")) {
    ssid = "OnePlusWout";
    password = "stoomboot";
  } else if(used_wifi.equals("home-wout")) {
    ssid = "bosstraat";
    password =  "wotikrko22";
  } else if(used_wifi.equals("howest-iot")) {
    ssid = "Howest-IoT";
    password =  "LZe5buMyZUcDpLY";
  }

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Connecting to WiFi..");
    led_on(0, 255, 242);
    delay(500);
  }

  Serial.println("Connected to the WiFi network");

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");

    led_on(255, 165, 0);
    buzzer(500);

    if (client.connect(TIK_HOSTNAME_ARR, mqttUser, mqttPassword)) {
      led_on(0, 255, 0);
      buzzer(800);
      led_of();

      Serial.print("connected as ");
      Serial.print(TIK_HOSTNAME);
      Serial.println();

      client.subscribe(TIK_SUBTOPIC_ARR);
      Serial.print("Client subscribed to: ");
      Serial.println(TIK_SUBTOPIC);
    }
  }


}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");

    led_on(255, 165, 0);
     buzzer(500);
   

    if (client.connect(TIK_HOSTNAME_ARR, mqttUser, mqttPassword)) {
      led_on(0, 255, 0);
      buzzer(800);
      led_of();

      Serial.println("connected");
      client.subscribe(TIK_SUBTOPIC_ARR);

      
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println("try again in 5 seconds");
      delay(1000);
    }
  }
}

void setup_touch() {
  for (int i = 0; i <= 100; i++) {
    touchGemiddelde += touchRead(touchPin);
  }
  touchGemiddelde = touchGemiddelde / 100;
}

void callback(char* topic, byte* payload, unsigned int length) {
  StaticJsonBuffer<300> jsonBuffer;
  Serial.println("CALLBACK");
  char inData[length];

  Serial.print("payload: ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    inData[(i)] = (char)payload[i];
  }

  JsonObject& root = jsonBuffer.parseObject(inData);

  if (!root.success()) { 
    Serial.println("Parsing failed");
    delay(1000);
    return;
  }

  int id = root["tik_id"];

  if (id == TIK_ID) {
    light_status = root["light_status"];

    red = root["red"];
    green = root["green"];
    blue = root["blue"];

    Tone = root["tone"];

    led_on(red, green, blue);

    buzzer(Tone);
  }

  Serial.println();
  Serial.print("ID: ");
  Serial.print(id);
  Serial.print('\t');
  Serial.print("Red: ");
  Serial.print(red);
  Serial.print('\t');
  Serial.print("Green: ");
  Serial.print(green);
  Serial.print('\t');
  Serial.print("Blue: ");
  Serial.print(blue);
  Serial.print('\t');
  Serial.print("Note: ");
  Serial.print(Tone);
  Serial.print('\t');
  Serial.println();
}


void setup() {
  Serial.begin(115200);
  setup_buzzer();
  setup_touch();
  setup_wifi();

}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  touchWaardeHuidig =  touchRead(touchPin);
  handle_touch_sensor();

}

void handle_touch_sensor() {
  if (!touchActive) {
    if ((touchGemiddelde - touchWaardeHuidig) > touchTreshold) {
      touchChangeCount++;
    }
    else {
      touchChangeCount = 0;
    }

    if (touchChangeCount > 5) {
      tik_status = true;
      update_status(tik_status);
      Serial.println("TOUCHED");
      
      touchChangeCount = 0;
      touchActive = true;
      ledcWriteTone(channel, 500);
    }
  }

  else {
    if ((touchGemiddelde - touchWaardeHuidig) < touchTreshold) {
      touchChangeCount++;
    }
    else {
      touchChangeCount = 0;
    }

    if (touchChangeCount > 50) {
      tik_status = false;
      update_status(tik_status);
      touchChangeCount = 0;
      touchActive = false;
      ledcWriteTone(channel, 0);
    }
  }
}

void update_status(boolean stat) {
  String data_raw = "{\"tik_id\":" + String(TIK_ID) +  ", \"tik_status\":" + String(stat)  + ", \"light_status\":" + String(light_status) + "}"; //+ ", \"red\":" + String(red) + ", \"green\":" + String(green) + ", \"blue\":" + String(blue) + "}";
  data_raw.toCharArray(raw_buffer, 200);
  client.publish(TIK_PUBTOPIC, raw_buffer);
}
