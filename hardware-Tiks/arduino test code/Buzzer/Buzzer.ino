int freq;
int channel = 0;
int resolution = 8;
const int buzzerPin = 26;
  
void setup() {
  Serial.begin(115200);
  ledcSetup(channel, freq, resolution);
  ledcAttachPin(buzzerPin, channel);
  ledcWrite(channel, 127);
  ledcWriteTone(channel, 0);
}
  
void loop() {
  if(Serial.available() > 0){
    freq = Serial.readString().toInt();
    ledcWriteTone(channel, freq);
  }
}
