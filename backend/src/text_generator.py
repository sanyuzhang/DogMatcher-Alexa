import random
from utter_more import UtterMore


TOPIC_UNKNOWN = -1
TOPIC_UNKNOWN = 0
TOPIC_EXP = 1
TOPIC_TIME = 2
TOPIC_HOME = 3
TOPIC_APT = 4
TOPIC_NOISE = 5
TOPIC_SHED = 6
TOPIC_KIDS = 7
TOPIC_ACT = 8

TOPIC_CARD_SPEECH = 11
TOPIC_CARD_TEXT = 12


def generate_topic(topic_id):
    if topic_id == TOPIC_EXP:
        um = UtterMore(
            "(Now|Please) tell me, (what is|what's) your experience with dogs?",
            "(Now|Please) tell me, have you ever (had|adopted) (a dog|dogs) before?",
            "(Are you familiar|Do you have experience) with raising (a dog|dogs)?"
        )
    elif topic_id == TOPIC_TIME:
        um = UtterMore(
            "How many hours (per|every) week (can|could) you (put into|spend on) (trainning|playing with) your dog?",
            "In general, what's the hours per week that you (put into|spend on) (trainning|playing with) your dog?"
        )
    elif topic_id == TOPIC_HOME:
        um = UtterMore(
            "Do you live in an apartment or a house?",
            "What kind of home do you live in, a house or an apartment?",
            "What is your living condition? Is it an apartment or a house?"
        )
    elif topic_id == TOPIC_APT:
        um = UtterMore(
            "Do you just want to see dogs that are suitable for (an apartment|apartments)?",
            "Would you like to see apartment dogs only?",
            "Would you only consider apartment dogs?"
        )
    elif topic_id == TOPIC_NOISE:
        um = UtterMore(
            "Would you like your dog to be quieter or more vocal?",
            "On a scale of one to five, with five being the highest, what's your tolerence level for barking?"
        )
    elif topic_id == TOPIC_SHED:
        um = UtterMore(
            "On a scale of one to five, with five being the highest, what's your tolerence level for shedding?",
            "What's your expectation of shedding, frequent or infrequent?"
        )
    elif topic_id == TOPIC_KIDS:
        um = UtterMore(
            "Do you have (kids|a kid) under ten?",
            "Do you have small kids at home?",
            "Do you want a kids-friendly dog?"
        )
    elif topic_id == TOPIC_ACT:
        um = UtterMore(
            "On a scale one to four, with four being the highest, what's your activity level?",
            "Do you excercise very often?",
            "How often do you excercise?"
        )
    elif topic_id = TOPIC_WELCOME:
        um = UtterMore(
            "(Greetings, this is|Welcome to) Dog Matcher. I (will|can) help you find a dream (dog|puppy). Let's (start|begin) with a question.",
            "(Hi|Hello), I'm Dog Matcher. (Let me|I will try my best to) find a dream (dog|puppy) for you. First, let's (start|begin) with a question.",
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


def generate_card_topic(topic_id, dog):
    if dog:
        dog_name = dog[1]
        dog_desc = dog[2].strip()
        if topic_id == TOPIC_CARD_SPEECH:
            um = UtterMore(
                "(Perfect|Yeah), I have found a best match for you. It is called " + dog_name,
                "(Great|Good news). I think " + dog_name + " is a best match for you.",
            )
        elif topic_id == TOPIC_CARD_TEXT:
            um = UtterMore(
                # TODO
                dog_desc,
            )
    else:
        um = UtterMore(
            "Sorry, I failed to find a matched dog for you.",
            "It seems very difficult to find a match for you."
        )
    um.iter_build_utterances()
    return random.choice(um.utterances)


def generate_card_utter(topic_id, dog):
    utter = generate_card_topic(topic_id, dog)
    return random.choice(utter)

def generate_clarification(topic_id):
    if topic_id == TOPIC_EXP:
        um = UtterMore(
            "To recommend you human friendly dog.",
        )
    elif topic_id == TOPIC_TIME:
        um = UtterMore(
            "If you have little time, I will recommend you the easy trained dog.",
        )
    elif topic_id == TOPIC_HOME:
        um = UtterMore(
            "Some dog need more space.",
        )
    elif topic_id == TOPIC_APT:
        um = UtterMore(
            "To recommend the suitable dog.",
        )
    elif topic_id == TOPIC_NOISE:
        um = UtterMore(
            "So that the barking sound does not bother you.",
        )
    elif topic_id == TOPIC_SHED:
        um = UtterMore(
            "So that I can recommend the dog shedding at your tolorance level.",
        )
    elif topic_id == TOPIC_KIDS:
        um = UtterMore(
            "If you have kids, I will recommend you kids-friendly dog.",
        )
    elif topic_id == TOPIC_ACT:
        um = UtterMore(
            "So that I can find the dog that suits your activity level best.",
        )
    else:
        um = UtterMore(
            "Sorry, I cannot understand.",
            "Sorry, I did not catch that.",
            "Sorry, can you speak it again?"
        )
    um.iter_build_utterances()
    return random.choice(random.choice(um.utterances))


if __name__ == '__main__':
    for i in range(0, 9):
        print(generate_utter(i))
