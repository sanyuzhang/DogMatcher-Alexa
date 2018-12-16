# call elaborate_result(dog)
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

def compareDogsSame(dog1, dog2, att):
    attValue = getattr(dog1, att) - 1
    ut = UtterMore(
        dog1.name + " and " + dog2.name + " (have the same " + ATT_STR[att][0] + "|" + ATT_STR[att][1] + "). They " + ATT_UNIT[att][attValue],
        
        dog1.name + " " + ATT_STR[att][2] + ". They " + ATT_UNIT[att][attValue],
    )
    return randomUtter(ut)

def compareDogsAnd(dog1, dog2, att):
    attValues = [getattr(dog1, att) - 1, getattr(dog2, att) - 1]
    ut = UtterMore(
        dog1.name + " " + ATT_UNIT[att][attValues[0]] + ", (while|and) " + 
        dog2.name + " " + ATT_UNIT[att][attValues[1]] + ".",
    )
    return randomUtter(ut)

def compareDogsOr(names, atts, unit, words):
    if atts[0] > atts[1]:
        # Swap
        atts[0], atts[1] = atts[1], atts[0]
        names[0], names[1] = names[1], names[0]
    
    ut = UtterMore(
        names[1] + " is " + str(atts[1]) + " " + unit + ". " + 
        names[0] + " is " + str(abs(atts[1] - atts[0])) + " " + unit + " " +
        words[0] + " than it.",

        names[1] + " is " + str(atts[1]) + " " + unit + ", while " + 
        names[0] + " is " + words[0] + " than it, which is " + str(atts[0]) + " " + unit,
        
        names[0] + " is " + str(atts[0]) + " " + unit + ". " + 
        names[1] + " is " + str(abs(atts[1] - atts[0])) + " " + unit + " " +
        words[1] + " than it.",

        names[0] + " is " + str(atts[0]) + " " + unit + ", while " + 
        names[1] + " is " + words[1] + " than it, which is " + str(atts[1]) + " " + unit,
    )
    return randomUtter(ut)
    


def compareDogs(dog1, dog2):
    res = ""
    # att = 'name'
    # names = [dog1[att].replace("Dog", ""), dog2[att].replace("Dog", "")]
    # att = 'weight_min'
    # weight_min = [dog1[att], dog2[att]]

    # return compareDogsOr(names, weight_min, "pound", ["lighter", "heavier"])

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
    res += randomUtter(ut)
    
    # Compare each attribute
    # dogAtts = list(dog1.__dict__.keys())
    # dogAtts.remove('name')
    dogAtts = ['size', 'actLvl', 'barkLvl', 'shed']
    # Group attributes by difference
    sameAtts = []
    diffAtts = []
    for att in dogAtts:
        if getattr(dog1, att) == getattr(dog2, att):
            sameAtts.append(att)
        else:
            diffAtts.append(att)
    
    for att in sameAtts:
        res += compareDogsSame(dog1, dog2, att)
    
    for att in diffAtts:
        res += compareDogsAnd(dog1, dog2, att)

    return res

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
    # Setup database access
    connection = sqlite3.connect("dogs.db3")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    # Get column names
    # cursor.execute("SELECT * FROM dogs")
    # colNames = cursor.fetchone().keys()
    
    # find dogs
    # cursor.execute("SELECT * FROM dogs WHERE id == 5 or id == 7")
    cursor.execute("SELECT * FROM dogs")
    rows = cursor.fetchall()
    
    #print(elaborate_result(dog[0]))
    dogs = []
    for row in rows:
        dogs.append(Dog(row))
        #print(dogs[-1])

    GetDogsDiffDistribution(dogs)
    
    dogNum = len(dogs)
    for i in range(10):
        ids = random.sample(range(dogNum), 2)
        print(compareDogs(dogs[ids[0]], dogs[ids[1]]))
    
