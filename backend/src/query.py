import sqlite3

############## get parameters ##############
# set default value to parameters
haveKids = True  # True or False
aptDog = True  # if see apt dogs only
trainTime = 5  # 1-5, 5 is the mostly easy trained
barkLevel = 5  # 1-5, 5 is likes to be vocal
shedLevel = 5  # 1-5, 5 is shredding regularly
activityLevel = 1  # 1-4, 4 is the laziest

# get user's requirements
# hadDog, trainTime etc..

############## filter dogs based on haveKids and aptDog ###############
connection = sqlite3.connect("dogs.db3")
cursor = connection.cursor()

charactReq = []  # 1-10, smalleset, smartest, family dog, kids' friend etc.
dogIds = []  # the ids of dogs who meet charactReq
if aptDog or haveKids:
    if aptDog:
        charactReq.append(9)  # best dogs for apt
    if haveKids:
        charactReq.append(8)  # best dogs for kids
        charactReq.append(6)  # best family dogs

    # fetch data from database
    cursor.execute("SELECT dog_id FROM dogs_characteristics WHERE characteristic_id \
                    IN (" + " ,".join(str(x) for x in charactReq) + ")")
    dogIds = cursor.fetchall()

if aptDog or haveKids:  # use dog_id for filter parameter
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
