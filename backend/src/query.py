from config import *
import sqlite3


############## get parameters ##############
# get user's requirements
# hadDog, trainTime etc..


############## filter dogs based on haveKids and aptDog ###############
def query(trainTime = 5, aptDog = True,  barkLevel = 5, shedLevel = 5, haveKids = True, activityLevel = 1):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    charactReq = [] # 1-10, smalleset, smartest, family dog, kids' friend etc.
    dogIds = [] # the ids of dogs who meet charactReq
    if aptDog or haveKids:
        if aptDog:
            charactReq.append(9) # best dogs for apt
        if haveKids:
            charactReq.append(8) # best dogs for kids
            charactReq.append(6) # best family dogs

    # fetch data from database
        cursor.execute("SELECT dog_id FROM dogs_characteristics WHERE characteristic_id \
                   IN (" + " ,".join(str(x) for x in charactReq) +")")
    dogIds = cursor.fetchall()

    if aptDog or haveKids: # use dog_id for filter parameter
        cursor.execute("SELECT * FROM dogs WHERE \
                       id IN (" + " ,".join(str(x[0]) for x in dogIds) + ")\
                       and activity_level >= " + str(activityLevel) + \
                       " and barking_level <= " + str(barkLevel) + \
                       " and shedding <= " + str(shedLevel) + \
                       " and trainability <= " + str(trainTime))
    else:
        cursor.execute("SELECT * FROM dogs WHERE\
                       activity_level >= " + str(activityLevel) + \
                       " and barking_level <= " + str(barkLevel) + \
                       " and shedding <= " + str(shedLevel) + \
                       " and trainability <= " + str(trainTime))
    result = cursor.fetchall()
    return result
