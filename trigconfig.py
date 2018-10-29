# Adds functionality for angle unit selection between degrees and radians.
import math


class TrigConfigurator:
    def __init__(self, use_degrees=False):
        self.use_degrees = use_degrees

    def set_mode(self, use_degrees):
        self.use_degrees = use_degrees

    def sin(self, num):
        return self._choose_func(math.sin, num)

    def cos(self, num):
        return self._choose_func(math.cos, num)

    def tan(self, num):
        return self._choose_func(math.tan, num)

    def _choose_func(self, func, num):
        if self.use_degrees:
            return _in_degrees(func, num)
        else:
            return func(num)


def _in_degrees(func, num):
    # Converts num from degrees into radians, then passes it into func and returns the result
    return func(math.radians(num))
