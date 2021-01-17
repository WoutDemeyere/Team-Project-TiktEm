import json
class Tik:
    def __init__(self,id,tikstatus,lightstatus,red,green,blue, tone, mqtt_client):
        self.id = id
        self.tikstatus = tikstatus
        self.lightstatus = lightstatus
        self.red = red
        self.green = green
        self.blue = blue
        self.tone = tone
        self.mqtt = mqtt_client
        self.colorhunt_status = False

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, nieuwid):
        if (nieuwid != ""):
            self._id = nieuwid
        else:
            raise ValueError("Geen geldig id, kan niet leeg zijn {}")

    @property
    def tikstatus(self):
        return self._tikstatus
    @tikstatus.setter
    def tikstatus(self, nieuwetikstatus):
        self._tikstatus = nieuwetikstatus

    @property
    def lightstatus(self):
        return self._lightstatus
    @lightstatus.setter
    def lightstatus(self, nieuwelightstatus):
        self._lightstatus = nieuwelightstatus

    @property
    def red(self):
        """The red property."""
        return self._red
    @red.setter
    def red(self, value):
        self._red = value

    @property
    def green(self):
        """The green property."""
        return self._green
    @green.setter
    def green(self, value):
        self._green = value

    @property
    def blue(self):
        """The blue property."""
        return self._blue
    @blue.setter
    def blue(self, value):
        self._blue = value
    
    @property
    def tone(self):
        """The tone property."""
        return self._tone
    @tone.setter
    def tone(self, value):
        self._tone = value
    
    def turn_on(self, red, green, blue, tone):
        self._lightstatus = True
        self._red = red
        self._green = green
        self._blue = blue
        self._tone = tone
        self.update()

    def turn_off(self):
        self._tikstatus = False
        self._lightstatus = False
        self._red = 0
        self._green = 0
        self._blue = 0
        self._tone = 0
        self.update()

    def update(self):
        data = {"tik_id":self.id, "tik_status":self.tikstatus, "light_status":self.lightstatus, "red":self.red, "green":self.green, "blue":self.blue, "tone":self.tone}
        data_raw = json.dumps(data)
        #print(f'tik: {self.id} : {data}')
        self.mqtt.publish(f'tiktem/tik{self.id}', data_raw)
