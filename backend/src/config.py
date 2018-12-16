import os

END_OF_QUESTION = 8

DIRECTION_QUESTIONS = {
    1: {
        # Have experience with dogs
        True: 2,
        # No previous experience
        False: 3
    },
    2: 3,
    3: {
        # Home is apartment
        True: 4,
        # Home is house with yard
        False: 5
    },
    4: {
        # Only dogs for apt
        True: 7,
        False: 5
    },
    5: 6,
    6: 7,
    7: 8,
}

QUESTION_PARAMETER = {
    2: "trainTime",
    4: "aptDog",
    5: "barkLevel",
    6: "shedLevel",
    7: "haveKids",
    8: "activityLevel"
}

DEFAULT_PARAMETER = {
    # 1-5, 5 is the mostly easy trained
    "trainTime": 5,
    # if see apt dogs only
    "aptDog": True,
    # 1-5, 5 is likes to be vocal
    "barkLevel": 5,
    # 1-5, 5 is shredding regularly
    "shedLevel": 5,
    # True or False
    "haveKids": True,
    # 1-4, 4 is the laziest
    "activityLevel": 1
}

ATTRIBUTE_STATE = "state"
ATTRIBUTE_DOG_PARAMETER = "para"

DB_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../../dogs.db3'