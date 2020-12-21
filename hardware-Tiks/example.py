import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import json
from codecs import encode

device="tik1"
def on_connect(client,userdata,flahs,rc):
    print("connected with result code "+str(rc))

def on_message(client,userdata,msg):
    #print(msg.topic+" "+ str(msg.payload))
    print(msg.payload)
    test=json.loads(msg.payload)    
    if(test["state"]=="on"):
        print("led aan")
    else:
        print("led uit")
    try:
        if(test["sound"]):
            print(test["sound"])
    except Exception as ex :
        pass
    
while True:
    client=mqtt.Client()
    client.on_connect=on_connect
    client.on_message=on_message
    client.connect("13.81.105.139",1883,60)
    client.subscribe(f"/project/tiktems/{device}")
    client.loop_forever()
    #dit moet wel async
    if(input()=="push"):
        #controle als led aan is dan uit doen 
        print("led uit")
        #send message to backend
    
    #
    #
    

    



