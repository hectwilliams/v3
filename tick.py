import numpy as np 
class Tick():
    def __init__(self) -> None:
        self.value = np.int16(0)
    def tick(self):
        prev_value = self.value
        self.value += 1
        return prev_value