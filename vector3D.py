import multiprocessing
import multiprocessing.managers
import multiprocessing.process
from decimal import Decimal
from math import sqrt
import numbers 

IP_ADDRESS='127.0.0.1'
PORT=50000
AUTHKEY=b'abcd'

class Vector3():
    def __init__(self,x=0, y=0, z=0):
        self.x=x
        self.y=y
        self.z=z
        self._type = Vector3
    def get(self):
        return self
    def set(self, vector3):
        for attr, _ in self.__dict__.items():
            self.__dict__[attr]=vector3.__dict__[attr]
    vector=property(get,set)
    def __repr__(self) -> str:
        return f'Vector3( x = { self.x }, y = { self.y }, z = { self.z } )'
    def zero(self):
        for attr, _ in self.__dict__.items():
            self.__dict__[attr]=0
    def __mul__(self, value):
        if isinstance(value, numbers.Number):
            return Vector3(self.x * value, self.y * value, self.z * value)
        if isinstance(value, Vector3):
            # dot product
            print("dot product")
            return self.x * value.x + self.y * value.y + self.z * value.z
        raise TypeError("Vector3 or scalar are permitted")
    def __rmul__(self, val):
        return self.__mul__(val)
    def __add__(self, value):
        if isinstance(value, numbers.Number):
            return Vector3(self.x + value, self.y + value, self.z + value)
        if isinstance(value, Vector3):
            return Vector3(self.x + value.x, self.y + value.y, self.z + value.z)
        raise TypeError("Vector3 or scalar are permitted")
    def __sub__(self, value):
        if isinstance(value, numbers.Number):
            return Vector3(self.x - value, self.y - value, self.z - value)
        if isinstance(value, Vector3):
            return Vector3(self.x - value.x, self.y - value.y, self.z - value.z)
        raise TypeError("Vector3 or scalar are permitted")
    def __truediv__(self, value):
        try:
            if isinstance(value, numbers.Number):
                return Vector3(self.x/value, self.y/value, self.z/value)
            if isinstance(value, Vector3):
                return Vector3(self.x / value.x, self.y / value.y, self.z / value.z)
            raise TypeError("Vector3 or scalar are permitted")
        except ZeroDivisionError as e:
            print("Divide by Zero Error")
    def __eq__(self, vector3) -> bool:
        return all([value == vector3.__dict__[attr] for attr,value in self.__dict__.items()] )
    def normalize(self) :
        print(self)
        mag_sq = self.x**2 + self.y**2 + self.z**2
        if mag_sq > 0:
            one_over_sqrt_mag = 1 / sqrt(mag_sq)
            print(one_over_sqrt_mag)
            self.x *= one_over_sqrt_mag
            self.y *= one_over_sqrt_mag
            self.z *= one_over_sqrt_mag

