/* ------------------------- IMPORTS ------------------ */
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

/* ------------------ TIK-ELEMENTS ------------------ */
int TIK_ID = 3;

String TIK_HOSTNAME = "Tiktem-Tik" + String(TIK_ID);
String TIK_SUBTOPIC = "tiktem/tik" + String(TIK_ID);
char TIK_HOSTNAME_ARR[20];
char TIK_SUBTOPIC_ARR[20];
char* TIK_PUBTOPIC = "tiktem/tiksout";
boolean tik_status = false;


/* ------------------- WIFI ------------------------ */
const String used_wifi = "hotspot-wout";           //"hotspot-wout", "howest-iot", "home-wout", "home-torre-moeder"
char* ssid = "";
char* password = "";
WiFiClient espClient;


/* -------------------- MQTT ------------------------ */
const char* mqttServer = "192.168.43.40";
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = "";
char raw_buffer[200];

PubSubClient client(espClient);


/* -------------------------- LED --------------------- */
const int LED_PIN = 15;
const int NUMPIXELS = 1;
Adafruit_NeoPixel pixels(NUMPIXELS, LED_PIN, NEO_RGB + NEO_KHZ800);

int red = 0;
int green = 0;
int blue = 0;

int brightness = 255;
int delay_on = 0;


/* ------------------------- BUZZER --------------------- */
int freq;
int channel = 0;
int resolution = 8;
const int buzzerPin = 26;
const int touchPin = 4;
int Tone = 0;

/* -------------------------- TOUCH ----------------------- */
int touchWaardeHuidig;
int touchChangeCount = 0;
bool touchActive = false;
int touchInActiveCount = 0;
int touchGemiddelde = 0;
int touchTreshold = 10;


/* ------------------------------------------------------------ */
/* -------------------------- FUNCTIONS ----------------------- */
/* ------------------------------------------------------------ */

/* --------------------------- SETUP ------------------------- */
void setup() {
  Serial.begin(115200);
  setup_buzzer();
  setup_touch();
  setup_wifi_mqtt();
}

void setup_buzzer() {
  ledcSetup(channel, freq, resolution);
  ledcAttachPin(buzzerPin, channel);
  ledcWrite(channel, 127);
  ledcWriteTone(channel, 0);
}

void setup_touch() {
  for (int i = 0; i <= 100; i++) {
    touchGemiddelde += touchRead(touchPin);
  }
  touchGemiddelde = touchGemiddelde / 100;
  Serial.print("TOUCH GEMIDDELDE: ");
  Serial.println(touchGemiddelde);
}


/* --------------------------- MQTT & WIFI ------------------------- */
void setup_wifi_mqtt() {     /* (& MQTT)*/
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
  } else if(used_wifi.equals("home-torre-moeder")) {
    ssid = "telenet-9239010";
    password = "C5paexkc6utp";
  }
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Connecting to WiFi..");
    led_on(0, 255, 242);
    delay(500);
  }
  Serial.println("Connected to the WiFi network");
  led_buzzer_delay(255, 165, 0, 500, 150);
  led_on(255, 165, 0);


  // CONNECTING TO MQTT
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
  
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    if (client.connect(TIK_HOSTNAME_ARR, mqttUser, mqttPassword)) {
      led_buzzer_delay(0, 255, 0, 800, 150);

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

    led_buzzer_delay(255, 0, 0, 3000, 2000);

    if (client.connect(TIK_HOSTNAME_ARR, mqttUser, mqttPassword)) {
      led_buzzer_delay(0, 255, 0, 800, 150);

      Serial.println("reconnected to mqtt");
      client.subscribe(TIK_SUBTOPIC_ARR);
    } 
    else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println("try again in 5 seconds");
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) { /* wordt opgeroepen als er een mqtt bericht binnen komt*/
  // DATA INLEZEN
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

  // DATA VERWERKEN
  if (id == TIK_ID) {     // extra controle
    red = root["red"];
    green = root["green"];
    blue = root["blue"];
    Tone = root["tone"];
    delay_on = root["delay_on"];

    // geef een delay waarde mee om even te biepen, een 0 voor de led/buzzer aan te laten
    if (delay_on == 0){
      led_on(red, green, blue);
      buzzer(Tone);
    }
    else{
      led_buzzer_delay(red, green, blue, Tone, delay_on);
    }
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
  Serial.print("Delay: ");
  Serial.print(delay_on);
  Serial.println();
}

void update_status(boolean stat) {      // bericht naar mqtt server sturen, wordt opgeroepen als de touch sensor van state veranderd 
  String data_raw = "{\"tik_id\":" + String(TIK_ID) +  ", \"tik_status\":" + String(stat)  + "}";
  data_raw.toCharArray(raw_buffer, 200);
  client.publish(TIK_PUBTOPIC, raw_buffer);
}


/* --------------------------- LOGIC FUNCTIONS ------------------------- */
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  handle_touch_sensor();
  delay(5);
}

void led_on(int r, int g, int b) {
  pixels.clear();
  pixels.setBrightness(brightness);
  pixels.setPixelColor(0, pixels.Color(r, g, b));
  pixels.show();
}

void led_off() {
  pixels.clear();
  pixels.setBrightness(0);
  pixels.setPixelColor(0, pixels.Color(0, 0, 0));
  pixels.show();
}

void buzzer(int buzz) {
  ledcWriteTone(channel, buzz);
}

void led_buzzer_delay (int r, int g, int b, int buzz, int delay_millisec){
  led_on(r, g, b);
  buzzer(buzz);
  delay(delay_millisec);
  led_off();
  buzzer(0);
}

void handle_touch_sensor() {
  touchWaardeHuidig =  touchRead(touchPin);
  
  if (!touchActive) {
    if ((touchGemiddelde - touchWaardeHuidig) > touchTreshold) {
      touchChangeCount++;
    }
    else {
      touchChangeCount = 0;
    }

    if (touchChangeCount > 5) {
      touchActive = true;
      update_status(touchActive);
      Serial.println("TOUCHED");
      touchChangeCount = 0;
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
      touchActive = false;
      update_status(touchActive);
      touchChangeCount = 0;
    }
  }
}
