"""
validation practice
"""

class Fridge:
    def __init__(self, is_open:bool=False,
                  capacity:int=10,
                  temperature:int=15):
        self.is_open = is_open
        self.capacity = capacity
        self.temperature = temperature
    
    @property
    def capacity(self):
        return self.capacity
    
    @capacity.setter
    def capacity(self,value):
        if not isinstance(value, int):
            raise TypeError("Capacity must be an integer")
        if value < 0:
            raise ValueError("Capacity cannot be negative")
        self.capacity= value

    @property
    def open_close(self):
        return self.is_open
    
    @open_close.setter
    def open_close(self,value):
        if not isinstance(value, bool):
            raise TypeError("Open/Close must be a boolean")
        self.is_open = value
