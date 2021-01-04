class Tik:
    def __init__(self,id,tikstatus,lightstatus,red,green,blue):
        self.id = id
        self.tikstatus = tikstatus
        self.lightstatus = lightstatus
        self.red = red
        self.green = green
        self.blue = blue

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, nieuwid):
        if (nieuwid != ""):
            self._id = nieuwid
        else:
            # self._naam = "onbekend"
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

