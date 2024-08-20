import multiprocessing
import multiprocessing.managers
import multiprocessing.process
from decimal import Decimal
from math import sqrt
import time 
import os 
import asyncio 
import py_compile
import hashlib 
import numbers 

IP_ADDRESS='127.0.0.1'
PORT=50000
AUTHKEY=b'abcd'

class Vector3:
    def __init__(self,x=0, y=0, z=0):
        self.x=x
        self.y=y
        self.z=z
    def getxyz(self):
        return (self.x, self.y, self.z) 
    def setxyz(self, value):
        self.x=value[0]
        self.y=value[1]
        self.z=value[2]
    vector=property(getxyz,setxyz)
    def __repr__(self):
        return f'Vector3( x = { self.x }, y = { self.y }, z = { self.z } )'
    def __mul__(self, value):
        return Vector3(self.x * value, self.y * value, self.z * value)
    def __rmul__(self, val):
        return self.__mul__(val)
    def __add__(self, value):
        return Vector3(self.x + value, self.y + value, self.z + value)
    def __sub__(self, value):
        return Vector3(self.x - value, self.y - value, self.z - value)
    def __truediv__(self, value):
        return Vector3(self.x/value, self.y/value, self.z/value)
            