#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

const int PIN = 15;
const int NUMPIXELS = 1;

const int tik_id = 0;
const String tik_id_str = String(tik_id);
boolean touched = false;

const String topic_str = "tiktem/tik" + tik_id_str;

int red = 0;
int green = 0;
int blue = 0;

int Tone = 0;

int light_status = false;
int tik_status = false;

const char* ssid = "bosstraat";
const char* password =  "wotikrko22";
//const char* ssid = "Howest-IoT";
//const char* password =  "LZe5buMyZUcDpLY";
//const char* ssid = "OnePlusWout";
//const char* password = "stoomboot";
const char* mqttServer = "192.168.0.111";
//const char* mqttServer = "Raspberry";
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = "";

int freq;
int channel = 0;
int resolution = 8;
const int buzzerPin = 26;
//const int touchPin = 4;

const int touchPin = 4;
int touchWaardeHuidig;
int touchChangeCount = 0;
bool touchActive = false;
int touchInActiveCount = 0;

WiFiClient espClient;
PubSubClient client(espClient);
//StaticJsonBuffer<300> jsonBuffer;

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_RGB + NEO_KHZ800);


void callback(char* topic, byte* payload, unsigned int length) {
  StaticJsonBuffer<300> jsonBuffer;
  Serial.println("CALLBACK");
  char inData[length];

  Serial.print("payload: ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    inData[(i)] = (char)payload[i];
  }
  //Serial.println(inData);

  JsonObject& root = jsonBuffer.parseObject(inData);

  if (!root.success()) {   //Check for errors in parsing
    Serial.println("Parsing failed");
    delay(2000);
    return;
  }

  int id = root["tik_id"];

  if (id == tik_id) {
    light_status = root["light_status"];
    //tik_status = root["tik_status"];

    red = root["red"];
    green = root["green"];
    blue = root["blue"];

    Tone = root["tone"];

    turn_on_led(red, green, blue);

    buzzer(Tone);

    //    if(light_status) {
    //      buzzer_correct();
    //    }
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

  ledcSetup(channel, freq, resolution);
  ledcAttachPin(buzzerPin, channel);
  ledcWrite(channel, 125);

  pixels.begin();
  setup_client();
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }

  client.loop();

  touchWaardeHuidig =  touchRead(touchPin);
  if (!touchActive) {
    if (touchWaardeHuidig < 60) {
      touchChangeCount++;
    }
    else {
      touchChangeCount = 0;
    }

    if (touchChangeCount > 5 && touched == false) {
      touchChangeCount = 0;
      touchActive = true;
      tik_status = true;

      char raw_buffer[200];
      String data_raw = "{\"tik_id\":" + tik_id_str +  ", \"tik_status\":" + String(tik_status) + ", \"light_status\":" + String(light_status) + ", \"red\":" + String(red) + ", \"green\":" + String(green) + ", \"blue\":" + String(blue) + "}";

      data_raw.toCharArray(raw_buffer, 200);
      Serial.println("TOUCHED");
      client.publish("tiktem/tiksout", raw_buffer);
      ledcWriteTone(channel, 1000);
    }
  }

  else {
    if (touchWaardeHuidig > 60) {
      touchChangeCount++;
    }
    else {
      touchChangeCount = 0;
    }

    if (touchChangeCount > 50) {
      touchChangeCount = 0;
      touchActive = false;
      ledcWriteTone(channel, 0);
    }
  }

//  if (touchRead(4) < 60 && touched == false) {
//    touched = true;
//    tik_status = true;
//
//    char raw_buffer[200];
//    String data_raw = "{\"tik_id\":" + tik_id_str +  ", \"tik_status\":" + String(tik_status) + ", \"light_status\":" + String(light_status) + ", \"red\":" + String(red) + ", \"green\":" + String(green) + ", \"blue\":" + String(blue) + "}";
//
//    data_raw.toCharArray(raw_buffer, 200);
//    Serial.println("TOUCHED");
//    client.publish("tiktem/tiksout", raw_buffer);
//    //buzzer_correct();
//  }
//
//  if (touchRead(4) > 60 && touched == true) {
//    tik_status = false;
//    touched = false;
//  }
}



void setup_client() {
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
    //turn_on_led(227, 218, 45);
  }
  Serial.println("Connected to the WiFi network");

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");

    led_not_connected();

    String client_name_str = "TiktemTik" + tik_id_str;
    char client_name[25];
    client_name_str.toCharArray(client_name, 25);

    if (client.connect(client_name, mqttUser, mqttPassword )) {
      led_connected();
      Serial.println("connected");

    }
  }

  char topic[25];
  topic_str.toCharArray(topic, 25);
  client.subscribe(topic);
  //client.subscribe("tiktem/tik0");
}

void led_not_connected() {
  blink_led(255, 165, 0, 2);
}

void led_connected() {
  ledcWriteTone(channel, 500);
  turn_on_led(0, 255, 0);
  delay(1000);
  turn_of_led();
  ledcWriteTone(channel, 0);
}

void turn_on_led(int r, int g, int b) {
  pixels.clear();
  pixels.setBrightness(30);
  pixels.setPixelColor(0, pixels.Color(r, g, b));
  pixels.show();

}

void turn_of_led() {
  pixels.clear();
  pixels.setBrightness(0);
  pixels.setPixelColor(0, pixels.Color(0, 0, 0));
  pixels.show();
}


void blink_led(int r, int g, int b, int count) {
  pixels.clear();
  pixels.setBrightness(80);
  for (int i = 0; i < count; i++) {
    pixels.setPixelColor(0, pixels.Color(r, g, b));
    pixels.show();
    delay(250);
    pixels.setPixelColor(0, pixels.Color(0, 0, 0));
    pixels.show();
    delay(250);
  }
  //pixels.clear();
}

void buzzer(int buzz) {
  ledcWriteTone(channel, buzz);
  delay(350);
  ledcWriteTone(channel, 0);
}

void buzzer_correct() {
  ledcWriteTone(channel, 750);
  delay(350);
  ledcWriteTone(channel, 0);
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Subscribe
      client.subscribe("esp32/output");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(2000);
    }
  }
}
