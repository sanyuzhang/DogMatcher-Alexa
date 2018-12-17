import os
from math import *
import json

SIZE_MAX = 5
ACTIVITY_MAX = 4
BARKING_MAX = 5
SHED_MAX = 5

with open(os.path.dirname(os.path.realpath(__file__)) + '/dogAtt.json') as f:
    DOG_ATT = json.load(f)

class Dog:
    def __init__(self, row):
        self.name = row['name'].replace("Dog", "")

        self.size = row['size']
        self.sizeN = (self.size - 1) / (SIZE_MAX - 1)
        
        self.actLvl = row['activity_level']
        self.actLvlN = (self.actLvl - 1) / (ACTIVITY_MAX - 1)
        
        self.barkLvl = row['barking_level']
        self.barkLvlN = (self.barkLvl - 1) / (BARKING_MAX - 1)
        
        self.shed = row['shedding']
        self.shedN = (self.shed - 1) / (SHED_MAX - 1)
    
    def __str__(self):
        return self.name + ": size=" + str(self.size) + \
            ", activity_level=" + str(self.actLvl) + \
            ", barking_level=" + str(self.barkLvl) + \
            ", shedding=" + str(self.shed)

def GetDogsDiff(dog1, dog2):
    # Calculate their normalized Euclidean distance
    return sqrt(pow(dog1.sizeN - dog2.sizeN, 2) + \
        pow(dog1.actLvlN - dog2.actLvlN, 2) + \
        pow(dog1.barkLvlN - dog2.barkLvlN, 2) + \
        pow(dog1.shedN - dog2.shedN, 2)) / 4

def GetDogsDiffCategory(dog1, dog2):
    diff = GetDogsDiff(dog1, dog2)
    if diff < 0.13:
        return 0
    elif diff >= 0.13 and diff < 0.21:
        return 1
    elif diff >= 0.21 and diff < 0.33:
        return 2
    else:
        return 3
