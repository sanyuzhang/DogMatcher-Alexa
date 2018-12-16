# call elaborate_result(dog)

import random
import sqlite3
from utter_more import UtterMore

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
    connection = sqlite3.connect("dogs.db3") 
    cursor = connection.cursor() 
    cursor.execute("SELECT characteristic_id FROM dogs_characteristics WHERE dog_id \
                    ==" + str(dog[0]))
    charactId = cursor.fetchone()
    # building utterance 
    conf = UtterMore(
        "(Abosolutely|Sure)!",
        "No problem!",
        "(I like this one too. |)Here you go!",
        "Here's detailed info about " + dog[1] + ".",
        "That's (an excellent|a great) choice."
    )
    des = UtterMore(
        dog[2] + "He stands between " + str(dog[3]) + " and " + str(dog[4]) + " inches, and weights maximum " +\
        str(dog[6]) + " pounds. The " + dog[1] + " " + dog[17] + " amoung the most popular dogs breeds. " +\
        "He is one of the " + character[charactId[0]] + " with a " + coat_type[dog[13]] + " haircoat and he sheds " + shed_level[dog[14]] +\
        ". " + dog[1] + " " + activity_level[dog[11]] + ", and " + trainability[dog[16]] + " when trainning."
    )
    com = UtterMore(
        "I'm sure he'll be a strong competitor for the best family member award in your house!"
        "I'm sure you'll like it!"
        "That's right, no animal can equal the " + dog[1]+ " as a pet."
    )
    return randomUtter(conf) + " " + randomUtter(des) + " " + randomUtter(com)

if __name__ == '__main__':
    connection = sqlite3.connect("dogs.db3") 
    cursor = connection.cursor() 
    cursor.execute("SELECT * FROM dogs WHERE id == 5")
    dog = cursor.fetchone()
    #print(dog)
    print(elaborate_result(dog))