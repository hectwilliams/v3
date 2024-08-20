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
    def __mul__(self, val):
        if type(val) in [float, int]:
            self.x =self.x*val
            self.y =self.y*val
            self.z =self.z*val
            return self
        elif [isinstance(ele, numbers.Number) for ele in val] ==[True, True, True] and len(val)==3:
            return self._callmethod('mult_tuple', (val,))
    def __rmul__(self, val):
        return self.__mul__(val)
   