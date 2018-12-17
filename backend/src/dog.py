import os
import json
from math import *


SIZE_MAX = 5
ACTIVITY_MAX = 4
BARKING_MAX = 5
SHED_MAX = 5


with open(os.path.dirname(os.path.realpath(__file__)) + '/dog_att.json') as f:
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
        return "%s: size=%s, activity_level=%s, barking_level=%s, shedding=%s" % (self.name, self.size, self.actLvl, self.barkLvl, self.shed)

def GetDogsDiff(dog1, dog2):
    # Calculate their normalized Euclidean distance
    return sqrt(pow(dog1.sizeN - dog2.sizeN, 2)
        + pow(dog1.actLvlN - dog2.actLvlN, 2)
        + pow(dog1.barkLvlN - dog2.barkLvlN, 2)
        + pow(dog1.shedN - dog2.shedN, 2)) / 4

def GetDogsDiffCategory(dog1, dog2):
    # put dogs into different category based on their
    # difference on feature space
    diff = GetDogsDiff(dog1, dog2)
    if diff < 0.13:
        return 0 # very similar
    elif diff >= 0.13 and diff < 0.21:
        return 1 # similar
    elif diff >= 0.21 and diff < 0.33:
        return 2 # somewhat different
    else:
        return 3 # very different
