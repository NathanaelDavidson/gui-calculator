# Adds functionality for angle unit selection between degrees and radians.
import math

class TrigConfigurator:
    def __init__(self, use_degrees=False):
        self.use_degrees = use_degrees

    def set_mode(self, use_degrees):
        self.use_degrees = use_degrees
    
    def sin(self, num):
        return self._choose_funct(math.sin, num)

    def cos(self, num):
        return self._choose_funct(math.cos, num)

    def tan(self, num):
        return self._choose_funct(math.tan, num)

    def _choose_funct(self, funct, num):
        if self.use_degrees:
            return self._in_degrees(funct, num)
        else:
            return funct(num)

    def _in_degrees(self, funct, num):
        return funct(math.radians(num))