import multiprocessing
import multiprocessing.managers
import multiprocessing.process
from decimal import Decimal
from math import sqrt
import numbers 
import numpy as np

class Vector3():
    def __init__(self,x=np.float64(0.0), y=np.float64(0.0), z=np.float64(0.0)):
        self.x=x
        self.y=y
        self.z=z
        self._type = Vector3
        self.index = 0
        self.data = [x,y,z]
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
    def __iter__(self):
        return self
        return (self.x, self.y, self.z)
    def __next__(self):
        if self.index < len(self.data):
            r = self.data[self.index]
            self.index += 1
            return r
        else:
            raise StopIteration()
    def __mul__(self, value):
        if isinstance(value, numbers.Number):
            return Vector3(self.x * value, self.y * value, self.z * value)
        if isinstance(value, Vector3):
            # dot product
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
            return Vector3( np.subtract(self.x, value.x), np.subtract(self.y, value.y), np.subtract(self.z, value.z))
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
            # must be an argument paramters passed a v3 component
        return all([value == vector3.__dict__[attr] for attr,value in self.__dict__.items()] )
    def normalize(self) :
        mag_sq = self.x**2.0 + self.y**2.0 + self.z**2.0
        if mag_sq > 0.0:
            one_over_sqrt_mag_sq = 1.0 / sqrt(mag_sq)
            self.x *= one_over_sqrt_mag_sq
            self.y *= one_over_sqrt_mag_sq
            self.z *= one_over_sqrt_mag_sq
    def to_numpy(self):
        return np.array([
            self.x,
            self.y, 
            self.z
        ], dtype=np.float32)
    def set_x(self, value: np.float32):
        self.x = value
    def set_y(self, value: np.float32):
        self.y = value
    def set_z(self, value: np.float32):
        self.z = value
    def rand(self, k=1, **kwargs):
        if 'rng' in kwargs:
            rng = kwargs['rng']
            self.x = rng.random()*k
            self.y = rng.random()*k
            self.z  = rng.random()*k
        else:
            self.x = np.random.random()*k
            self.y = np.random.random()*k
            self.z = np.random.random()*k
    def copy(self):
        return Vector3(self.x, self.y, self.z)
# NonMember Functions
def vector_mag(vector: Vector3):
    return vector.x**2 + vector.y**2 + vector.z**2

def cross_product(v1: Vector3, v2: Vector3):
    return Vector3 (
            v1.y*v2.z - v1.z*v2.y ,
            v1.z*v2.x - v1.x*v2.z , 
            v1.x*v2.y - v1.y*v2.x 
    )
def distance(v1: Vector3, v2: Vector3):
    """Distance between two points(i.e vector points)"""
    dx = v1.x - v2.x
    dy = v1.y - v2.y
    dz = v1.z - v2.z
    return sqrt(dx**2 + dy**2 + dz**2)