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
        )
    elif topic_id == TOPIC_TIME_ID:
        um = UtterMore(
            "How many hours (per|every) week (can|could) you (put into|spend on) (trainning|playing with) your dog?"
        )
    elif topic_id == TOPIC_HOME_ID:
        um = UtterMore(
            "Do you live in an apartment or a house?",
            "What kind of home do you live in, a house or an apartment?"
        )
    elif topic_id == TOPIC_APT_ID:
        um = UtterMore(
            "sample..."
        )
    elif topic_id == TOPIC_NOISE_ID:
        um = UtterMore(
            "sample..."
        )
    elif topic_id == TOPIC_SHED_ID:
        um = UtterMore(
            "sample..."
        )
    elif topic_id == TOPIC_KIDS_ID:
        um = UtterMore(
            "sample..."
        )
    elif topic_id == TOPIC_ACT_ID:
        um = UtterMore(
            "sample..."
        )
    else:
        um = UtterMore(
            "sample..."
        )
    um.iter_build_utterances()
    return random.choice(um.utterances)


def generate_utter(topic_id):
    utter = generate_topic(topic_id)
    return random.choice(utter)


if __name__ == '__main__':
    for i in range(0, 9):
        print(generate_utter(i))