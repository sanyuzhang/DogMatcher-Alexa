import random
from utter_more import UtterMore


TOPIC_UNKNOWN = 0
TOPIC_EXP_ID = 1
TOPIC_TIME_ID = 2
TOPIC_HOME_ID = 3
TOPIC_APT_ID = 4
TOPIC_NOISE_ID = 5
TOPIC_SHED_ID = 6
TOPIC_KIDS_ID = 7
TOPIC_ACT_ID = 8


def generate_topic(topic_id):
    if topic_id == TOPIC_EXP_ID:
        um = UtterMore(
            "(Now|Please) tell me, (what is|what's) your experience with dogs?",
            "(Now|Please) tell me, have you ever (had|adopted) (a dog|dogs) before?",
            "(Are you familiar|Do you have experience) with raising (a dog|dogs)?"
        )
    elif topic_id == TOPIC_TIME_ID:
        um = UtterMore(
            "How many hours (per|every) week (can|could) you (put into|spend on) (trainning|playing with) your dog?",
            "In general, what's the hours per week that you (put into|spend on) (trainning|playing with) your dog?"
        )
    elif topic_id == TOPIC_HOME_ID:
        um = UtterMore(
            "Do you live in an apartment or a house?",
            "What kind of home do you live in, a house or an apartment?",
            "What is your living condition? Is it an apartment or a house?"
        )
    elif topic_id == TOPIC_APT_ID:
        um = UtterMore(
            "Do you just want to see dogs that are suitable for (an apartment|apartments)?",
            "Would you like to see apartment dogs only?",
            "Would you only consider apartment dogs?"
        )
    elif topic_id == TOPIC_NOISE_ID:
        um = UtterMore(
            "Would you like your dog to be quieter or more vocal?",
            "On a scale of one to five, with five being the highest, what's your tolerence level for barking?"
        )
    elif topic_id == TOPIC_SHED_ID:
        um = UtterMore(
            "On a scale of one to five, with five being the highest, what's your tolerence level for shedding?",
            "What's your expectation of shedding, frequent or infrequent?"
        )
    elif topic_id == TOPIC_KIDS_ID:
        um = UtterMore(
            "Do you have (kids|a kid) under ten?",
            "Do you have small kids at home?",
            "Do you want a kids-friendly dog?"
        )
    elif topic_id == TOPIC_ACT_ID:
        um = UtterMore(
            "On a scale one to four, with four being the highest, what's your activity level?",
            "Do you excercise very often?",
            "How often do you excercise?"
        )
    else:
        um = UtterMore(
            "Sorry, I don't understand.",
            "Sorry, I did not catch that.",
            "Sorry, can you speak it again?",
            "Say that one more time?"
        )
    um.iter_build_utterances()
    return random.choice(um.utterances)


def generate_utter(topic_id):
    utter = generate_topic(topic_id)
    return random.choice(utter)


if __name__ == '__main__':
    for i in range(0, 9):
        print(generate_utter(i))