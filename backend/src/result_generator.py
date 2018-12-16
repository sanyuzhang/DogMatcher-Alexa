# call elaborate_result(dog)
import random
import sqlite3
from utter_more import UtterMore
from config import *


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


if __name__ == '__main__':
    # test
    connection = sqlite3.connect(DB_PATH) 
    cursor = connection.cursor() 
    cursor.execute("SELECT * FROM dogs")
    dogs = cursor.fetchall()
    print(elaborate_result(dogs))