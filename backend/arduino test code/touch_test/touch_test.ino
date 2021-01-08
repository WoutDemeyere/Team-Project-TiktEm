int freq;
int channel = 0;
int resolution = 8;
const int buzzerPin = 26;
const int touchPin = 4;
int touchWaardeHuidig;
int touchChangeCount = 0;
bool touchActive = false;
int touchInActiveCount = 0;

void setup() {
  Serial.begin(115200);
  ledcSetup(channel, freq, resolution);
  ledcAttachPin(buzzerPin, channel);
  ledcWrite(channel, 127);
  ledcWriteTone(channel, 0);
}

void loop() {
  touchWaardeHuidig =  touchRead(touchPin);
  if (!touchActive){
    if (touchWaardeHuidig < 30) {
      touchChangeCount++;
    }
    else {
      touchChangeCount = 0;
    }
    
    if (touchChangeCount > 5) {
      touchChangeCount = 0;
      touchActive = true;
      ledcWriteTone(channel, 500);
    }
  }
  
  else {
    if (touchWaardeHuidig > 30) {
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
  delay(1);
}
