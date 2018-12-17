import random
from utter_more import UtterMore


TOPIC_UNKNOWN = -1
TOPIC_WELCOME = 0
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


def generate_utter(topic_id):
    if topic_id == TOPIC_EXP:
        um = UtterMore(
            "(Tell me, |)(what is|what's) your experience with dogs?",
            "(Tell me, |)have you ever (had|adopted) (a dog|dogs) before?",
            "(Are you familiar|Do you have experience) with raising (a dog|dogs)?"
        )
    elif topic_id == TOPIC_TIME:
        um = UtterMore(
            "(Got it|Gotcha|I see|OK|Roger that|Good). How many hours (per|every) week (can|could) you (put into|spend on) (trainning|playing with) your dog?",
            "(Got it|Gotcha|I see|OK|Roger that|Good). In general, what's the hours per week that you (put into|spend on) (trainning|playing with) your dog?"
        )
    elif topic_id == TOPIC_HOME:
        um = UtterMore(
            "(Got it|Gotcha|I see|OK|Roger that|Good). Do you live in an apartment or a house?",
            "(Got it|Gotcha|I see|OK|Roger that|Good). What kind of home do you live in, a house or an apartment?",
            "(Got it|Gotcha|I see|OK|Roger that|Good). What is your living condition? Is it an apartment or a house?"
        )
    elif topic_id == TOPIC_APT:
        um = UtterMore(
            "(Got it|Gotcha|I see|OK|Roger that|Good). Do you just want to see dogs that are suitable for (an apartment|apartments)?",
            "(Got it|Gotcha|I see|OK|Roger that|Good). Would you like to see apartment dogs only?",
            "(Got it|Gotcha|I see|OK|Roger that|Good). Would you only consider apartment dogs?"
        )
    elif topic_id == TOPIC_NOISE:
        um = UtterMore(
            "(Got it|Gotcha|I see|OK|Roger that|Good). Would you like your dog to be quieter or more vocal?",
            "(Got it|Gotcha|I see|OK|Roger that|Good). On a scale of one to five, with five being the highest, what's your tolerence level for barking?"
        )
    elif topic_id == TOPIC_SHED:
        um = UtterMore(
            "(Got it|Gotcha|I see|OK|Roger that|Good). On a scale of one to five, with five being the highest, what's your tolerence level for shedding?",
            "(Got it|Gotcha|I see|OK|Roger that|Good). What's your expectation of shedding, frequent or infrequent?"
        )
    elif topic_id == TOPIC_KIDS:
        um = UtterMore(
            "(Got it|Gotcha|I see|OK|Roger that|Good). Do you have (kids|a kid) under ten?",
            "(Got it|Gotcha|I see|OK|Roger that|Good). Do you have small kids at home?",
            "(Got it|Gotcha|I see|OK|Roger that|Good). Do you want a kids-friendly dog?"
        )
    elif topic_id == TOPIC_ACT:
        um = UtterMore(
            "(Got it|Gotcha|I see|OK|Roger that|Good). On a scale one to four, with four being the highest, what's your activity level?",
            "(Got it|Gotcha|I see|OK|Roger that|Good). Do you excercise very often?",
            "(Got it|Gotcha|I see|OK|Roger that|Good). How often do you excercise?"
        )
    elif topic_id == TOPIC_WELCOME:
        um = UtterMore(
                       "Welcome" #to DogMatcher, a tool that help you find the most suitable furry friend. \
                       I’ll first chat with you about your lifestyle then give you recommendation of dog breeds\
                       based on your habits. Please keep in mind that you can ask for clarification at any time. \
                       Now let’s start with a simple question,
        )
    else:
        um = UtterMore(
            "Sorry, I don't understand.",
            "Sorry, I did not catch that.",
            "Sorry, can you speak it again?",
            "Say that one more time?"
        )
    um.iter_build_utterances()
    return random.choice(random.choice(um.utterances))


def generate_card_utter(topic_id, dog):
    if dog:
        dog_name = dog[1]
        dog_desc = dog[2].strip()
        if topic_id == TOPIC_CARD_SPEECH:
            um = UtterMore(
                "(Perfect|Great|Excellent), based on your life habbits, I have found the top\
                 5 matches for you. You can ask more information for a particular breed or ask\
                 me to compare between two breeds.",
            )
        elif topic_id == TOPIC_CARD_TEXT:
            um = UtterMore(
                # TODO
                dog_desc,
            )
    else:
        um = UtterMore(
            "Sorry, (I could not find a matched dog based on your life habbits|\
            It seems very difficult to find a perfect match for you). Try to alter your\
             criteria, and when you are ready, give it another try.",
        )
    um.iter_build_utterances()
    return random.choice(random.choice(um.utterances))


def generate_clarification(topic_id):
    if topic_id == TOPIC_EXP:
        um = UtterMore(
            "(If you are not familar with dogs, you might not Know what to \
            expect after your new dog comes home|Before you master the basics of \
            dog care, you might be little bit overwhelmed as a first-time dog owner|It can be exciting to bring\
             a new dog into your home but it also can be a nerve-racking experience|\
             For someone deciding to get their very first dog, there can be quite a learning curve|\
            Some types of dogs will be much better suited towards first-time owners than others).\
              By getting to know your experience, I can modify the range of my search.",
            ""
        )
    elif topic_id == TOPIC_TIME:
        um = UtterMore(
            "(Dogs have different temperament|Training a dog can be a tedious task.) \
            Some breeds take to training better than others. If you don't plan to spend\
             a lot of time in training, I'll find you the one that is eager to please you!",
        )
    elif topic_id == TOPIC_HOME:
        um = UtterMore(
            "When you live in an apartment, it's important to consider your neighbors.\
             Some dogs tends to bark than others \
             so it's important to take that into consideration",
            "For people who live in close quarters with others or simply prefer \
             quiet, it’s necessary to find a dog breed that quieter at home.",
            "Because if you live in an apartment or simply hate 4 a.m. baying,\
             finding a peaceful pup is very necessary.",
        )
    elif topic_id == TOPIC_APT:
        um = UtterMore(
             "(For people who live in close quarters with others or simply prefer \
             quiet, it’s necessary to find a dog breed that quieter at home. By replying yes\
             , I'll find you those kind.",
            "Because by saying no, which means that the size and the barking level of a dog \
            doesn't bother you, I can offer you a greater variety of choices.",
        )
    elif topic_id == TOPIC_NOISE:
        um = UtterMore(
            "Dog bark could be (disturbing|annoying) sometimes. By asking this, I can avoid the\
            breeds that are beyound your tolerence.",
            "There are certain breeds that are more prone to barking than others. If you don't like\
              dog, I'll cross those out from my list."
        )
    elif topic_id == TOPIC_SHED:
        um = UtterMore(
            "Dog shedding could be (disturbing|annoying) sometimes. By asking this, I can avoid the\
            breeds that are beyound your tolerence.",
            "There are certain breeds that are more prone to shed than others. If you don't like\
             a dog leaves much of his hair behind on your belongings, I'll cross it from my list."
        )
    elif topic_id == TOPIC_KIDS:
        um = UtterMore(
            "If you have small kids, you should definitely be looking for a dog with \
            agreeable temperament. (For instance, a calmer dog has the ability \
            to form strong bonds and be a great companion for your kids|\
            Fun fact: Fierce-looking Boxers are considered good with children, \
            as are pit bulls. While Small, delicate, and potentially snappy dogs \
            such as Chihuahuas aren't so family-friendly).",
        )
    elif topic_id == TOPIC_ACT:
        um = UtterMore(
            "Different people have different energy level, so do dogs. (If you're a \
            couch potato, I would not consider a high-energy dog \
            breed who needs intense exercise|Whether your dog\
             is incredibly high-energy or a lump that prefers to lay around). It’s important\
             that his energy level is the same or lower than yours or your household’s.",
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
    for i in range(-1, 9):
        print(generate_utter(i))
