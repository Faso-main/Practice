""""
Open close principal (close to cahnges, but ipen for midification)
"""

import abc

class Furniture(abc.ABC):
    @abc.abstractmethod
    def __init__(self): pass
    
    @abc.abstractmethod
    def open_close(self): pass

class Fridge(Furniture):
    def __init__(self, is_open: bool, capacity: int, temperature: int):
        self.is_open = is_open if is_open else False
        self.capacity = capacity
        self.temperature = temperature

snippet1=Fridge()

