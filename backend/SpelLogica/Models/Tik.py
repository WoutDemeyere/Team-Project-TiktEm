import json


class Tik:
    def __init__(self, id, tikstatus, red, green, blue, tone, mqtt_client):
        self.id = id
        self.tikstatus = tikstatus
        self.red = red
        self.green = green
        self.blue = blue
        self.tone = tone
        self.mqtt = mqtt_client
        self.delay_on = 0
        self.batt_level = 0

        # colorteam
        self.in_use_colorTeam = False

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

    @property
    def delay_on(self):
        """The delay_on property."""
        return self._delay_on
    @delay_on.setter
    def delay_on(self, value):
        self._delay_on = value

    @property
    def batt_level(self):
        """The batt_level property."""
        return self._batt_level
    @batt_level.setter
    def batt_level(self, value):
        self._batt_level = value

    def tik_is_touched_signaal(self):
        self.turn_on_delay(0, 255, 255, 1000, 100)
    
    def turn_on(self, red, green, blue, tone):
        self.red = red
        self.green = green
        self.blue = blue
        self.tone = tone
        self.delay_on = 0
        self.update()

    def turn_on_delay(self, red, green, blue, tone, delay_millis):
        self.red = red
        self.green = green
        self.blue = blue
        self.tone = tone
        self.delay_on = delay_millis
        self.update()

    def turn_off(self):
        self.tikstatus = False
        self.red = 0
        self.green = 0
        self.blue = 0
        self.tone = 0
        self.delay_on = 0
        self.update()

    def update(self):
        data = {"tik_id": self.id, "red": self.red, "green": self.green, "blue": self.blue, "tone": self.tone, "delay_on": self.delay_on}
        data_raw = json.dumps(data)
        #print(f'tik: {self.id} : {data}')
        self.mqtt.publish(f'tiktem/tik{self.id}', data_raw)
    
