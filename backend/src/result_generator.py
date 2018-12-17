# call elaborate_result(dog)

import os
import random
import sqlite3
from utter_more import UtterMore
from config import *
from dog import *

activity_level = ["","needs a lot of excercise","needs regular excercise","is energetic","is calm"]
barking_level = ["","barks when necessary","doesn't like barking very much","tends to bark sometimes","barks frequently","likes to be vocal"]
shed_level = ["","infrequently","seasonally","frequently","occasionally","regularly"]
trainability = ["", "maybe stubborn", "is agreeable", "is eager to please", "is independet", "is easy to train"]
character = ["", "smallest dog breeds", "medium dog breeds", "largest dog breeds", "smartest dogs", "hypoallergenic dogs", "best family dogs", "best guard dogs", "best dogs for kids", "best dogs for apartments dwellers", "hairless dog breeds"]
coat_type = ["","hairless","short","medium","long","smooth","wire"]


def randomUtter(utters):
    utters.iter_build_utterances()    
    return random.choice(random.choice(utters.utterances))


def elaborate_result(dog):
    '''
    This function generates a description of dog given its info
        dog - tuple, contains dog's info
        output - String, desciption of the dog
    '''
    # get characteristic_id for the dog
    dog_id = dog[0]
    dog_name = dog[1]
    dog_desc = dog[2]
    dog_height_min = dog[3]
    dog_height_max = dog[4]
    dog_weight_min = dog[5]
    dog_weight_max = dog[6]
    dog_activity = activity_level[dog[11]]
    dog_coat = coat_type[dog[13]]
    dog_shed = shed_level[dog[14]]
    dog_train = trainability[dog[16]]
    dog_popularity = dog[17]

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor() 
    cursor.execute("SELECT characteristic_id FROM dogs_characteristics WHERE dog_id == %s" % (dog_id))
    charactId = cursor.fetchone()

    # building utterance 
    conf = UtterMore(
        "(Abosolutely|Sure)!",
        "No problem!",
        "I like this one too. Here you go!",
        "Here's detailed info about %s." % (dog_name),
        "That's (an excellent|a great) choice."
    )

    content = dog_desc

    if dog_height_min and dog_height_max:
        content += " %s stands between %s and %s inches." % (dog_name, dog_height_min, dog_height_max)
    elif dog_height_min:
        content += " %s stands at least %s inches." % (dog_name, dog_height_min)
    elif dog_height_max:
        content += " %s stands at most %s inches." % (dog_name, dog_height_max)
    if dog_weight_min and dog_weight_max:
        content += " And he weights between %s and %s pounds." % (dog_weight_min, dog_weight_max)
    elif dog_weight_min:
        content += " And he weights minimum %s pounds." % (dog_weight_min)
    elif dog_weight_max:
        content += " And he weights maximum %s pounds." % (dog_weight_max)
    if dog_popularity:
        content += " %s %s amongst the most popular American dogs breeds." % (dog_name, dog_popularity)
    if charactId:
        dog_charac = character[charactId[0]]
    else:
        dog_charac = character[0]
    if dog_charac and dog_coat:
        content += " He is one of the %s with a %s haircoat." % (dog_charac, dog_coat)
    elif dog_charac:
        content += " He is one of the %s." % (dog_charac)
    elif dog_coat:
        content += " He has %s haircoat." % (dog_coat)
    if dog_shed:
        content += " And he sheds %s." % (dog_shed)
    if dog_activity and dog_train:
        content += " %s %s , and %s when trainning." % (dog_name, dog_activity, dog_train)
    elif dog_activity:
        content += " %s %s." % (dog_name, dog_activity)
    elif dog_train:
        content += " %s %s when trainning." % (dog_name, dog_train)

    des = UtterMore(
        content
    )
    com = UtterMore(
        " I'm sure he'll be a strong competitor for the best family member award in your house!",
        " I'm sure you'll like it!",
        " That's right, no animal can equal the %s as a pet." % (dog_name),
    )
    return randomUtter(conf) + " " + randomUtter(des) + " " + randomUtter(com)

def compareDogsSameAll(dog1, dog2, atts):
    utStr = "They both"
    attNum = len(atts)
    for i in range(attNum - 1):
        utStr += " " + DOG_ATT[atts[i]]["units2"][getattr(dog1, atts[i]) - 1] + ", "
    utStr += " and " + DOG_ATT[atts[-1]]["units2"][getattr(dog1, atts[-1]) - 1]  + "."
    ut = UtterMore(
        utStr,
    )
    return randomUtter(ut)

def compareDogsSame(dog1, dog2, att):
    attValue = getattr(dog1, att) - 1
    ut = UtterMore(
        dog1.name + " and " + dog2.name + 
        " have the same " + DOG_ATT[att]["name"] + 
        ". They both " + DOG_ATT[att]["units2"][attValue],
        
        dog1.name + " " + DOG_ATT[att]["verb"][0] + " as " + DOG_ATT[att]["adj"][0] + " as " + dog2.name + 
        ". They both " + DOG_ATT[att]["units2"][attValue],
    )
    return randomUtter(ut) + "."

def compareDogsAnd(dog1, dog2, att):
    attValues = [getattr(dog1, att) - 1, getattr(dog2, att) - 1]
    connective = "and" if abs(attValues[0] - attValues[1]) < 2 else "(but|while)"
    ut = UtterMore(
        "(For the " + DOG_ATT[att]["name"] + ", |)" + 
        dog1.name + " " + DOG_ATT[att]["units1"][attValues[0]] + ", " + connective + " " + 
        dog2.name + " " + DOG_ATT[att]["units1"][attValues[1]] + ".",
    )
    return randomUtter(ut)

def compareDogs(dog1, dog2):
    res = ""
    conf = UtterMore(
        "(Abosolutely|Sure)!",
        "No problem!",
        "Here you go!",
        "Comparing " + dog1.name + " and " + dog2.name + ",",
    )
    res += randomUtter(conf) + " "
    # Get overall difference
    diff = GetDogsDiffCategory(dog1, dog2)
    if diff == 0:
        ut = UtterMore(
            dog1.name + " is very similar to " + dog2.name,
        )
    elif diff == 1:
        ut = UtterMore(
            dog1.name + " is similar to " + dog2.name,
        )
    elif diff == 2:
        ut = UtterMore(
            dog1.name + " is somewhat different to " + dog2.name,
        )
    else:
        ut = UtterMore(
            dog1.name + " is very different to " + dog2.name,
        )
    res += randomUtter(ut) + ". "
    
    # Compare each attribute
    dogAtts = ['size', 'actLvl', 'barkLvl', 'shed'] 
    # Group attributes by difference
    sameAtts = []
    diffAtts = []
    for att in dogAtts:
        if getattr(dog1, att) == getattr(dog2, att):
            sameAtts.append(att)
        else:
            diffAtts.append(att)

    if len(sameAtts) > 1: # if two dogs have more than one attribute that have the same value
        res += compareDogsSameAll(dog1, dog2, sameAtts) + " "
    elif len(sameAtts) == 1:
        res += compareDogsSame(dog1, dog2, sameAtts[0]) + " "
    
    for att in diffAtts:
        res += compareDogsAnd(dog1, dog2, att) + " "
    
    com = UtterMore(
        " I like " + dog1.name + " better, but both of them make a great pet!",
        " Either of them make a great pet!",
        " I'm sure you would love either of them!",
    )
    res += randomUtter(com)

    return res

def compareDogRows(row1, row2):
    return compareDogs(Dog(row1), Dog(row2))

def GetDogsDiffDistribution(dogs):
    dogGroups = {"very similar":0, "similar":0, "different":0, "very different":0}
    dogNum = len(dogs)
    for i in range(dogNum):
        for j in range(i + 1, dogNum):
            diff = GetDogsDiffCategory(dogs[i], dogs[j])
            if diff == 0:
                dogGroups["very similar"] += 1
            elif diff == 1:
                dogGroups["similar"] += 1
            elif diff == 2:
                dogGroups["different"] += 1
            else:
                dogGroups["very different"] += 1
    print(dogGroups)

if __name__ == '__main__':
    # testing
    # Setup database access
    DB_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../../dogs.db3'
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    # Get column names
    # cursor.execute("SELECT * FROM dogs")
    # colNames = cursor.fetchone().keys()
    
    # find dogs
    # cursor.execute("SELECT * FROM dogs WHERE id == 5 or id == 7")
    cursor.execute("SELECT * FROM dogs")
    rows = cursor.fetchall()

    # 
    dogs = []
    for row in rows:
        dogs.append(Dog(row))

    GetDogsDiffDistribution(dogs)
    
    dogNum = len(dogs)
    for i in range(1):
        ids = random.sample(range(dogNum), 2)
        print(ids)
        print(compareDogs(dogs[ids[0]], dogs[ids[1]]))
    
