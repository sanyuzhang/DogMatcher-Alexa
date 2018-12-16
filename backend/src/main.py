# Backend for DogMatcher alexa skill

import logging

from flask import Flask
from flask_ask import Ask, statement, question, session

from text_generator import generate_utter

app = Flask(__name__)
ask = Ask(app, "/")
log = logging.getLogger('flask_ask').setLevel(logging.DEBUG)

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
    7: 8
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

"""
Getter/Setter
"""


# Session Attributes Getter/Setter
def get_session_attr(attr):
    return session.attributes[attr]


def set_session_attr(key, value):
    session.attributes[key] = value


# state Getter/Setter
def set_state(state):
    set_session_attr(ATTRIBUTE_STATE, state)


def get_state():
    return get_session_attr(ATTRIBUTE_STATE)


# Dog Parameter Getter/Setter
def set_dog_parameter(para, value):
    parameters = get_session_attr(ATTRIBUTE_DOG_PARAMETER)
    parameters[para] = value
    set_session_attr(ATTRIBUTE_DOG_PARAMETER, parameters)


def get_dog_parameter(para):
    return get_session_attr(ATTRIBUTE_DOG_PARAMETER)[para]


"""
Handle user intent
"""


def user_update_dog_parameter(value):
    # record answer
    # first, find out which question is user answering
    prev_state = get_state()

    # second, find out what parameter does that question leads to
    if prev_state not in QUESTION_PARAMETER:
        return
    parameter = QUESTION_PARAMETER[prev_state]

    # finally, store new value to this parameter
    set_dog_parameter(parameter, value)


def user_answer_binary_question(ans):
    user_update_dog_parameter(ans)

    # change state
    prev_state = get_state()
    directions = DIRECTION_QUESTIONS[prev_state]

    # get next state
    if type(directions) == int:
        next_state = directions
    else:
        next_state = directions[ans]

    set_state(next_state)

    # get next question
    speech_text = generate_utter(get_state())

    return question(speech_text).reprompt(speech_text)


def user_answer_numeric_question(num):
    user_update_dog_parameter(num)

    # change state
    prev_state = get_state()
    next_state = DIRECTION_QUESTIONS[prev_state]
    set_state(next_state)

    # get next question
    speech_text = generate_utter(get_state())

    return question(speech_text).reprompt(speech_text)


'''
ASK Intent Entries
'''


@ask.on_session_started
def new_session():
    log.info('Dog Matcher skill new session started')


# @app.route("/", methods=["POST", "GET"])
@ask.launch
def launch():
    # init state
    set_state(1)

    # init parameters for later SQL query
    set_session_attr(ATTRIBUTE_DOG_PARAMETER, DEFAULT_PARAMETER)

    speech_text = "Welcome to the Dog Matcher skill, I will help you find your dream dog. Let's begin with a simple question. "

    speech_text += generate_utter(1)

    reprompt = speech_text

    return question(speech_text).reprompt(reprompt)


@ask.intent('user_confirm')
def intent_user_confirm():
    return user_answer_binary_question(True)


@ask.intent('user_deny')
def intent_user_deny():
    return user_answer_binary_question(False)


@ask.intent('user_numeric')
def intent_user_numeric(number):
    return user_answer_numeric_question(number)


@ask.intent('AMAZON.FallbackIntent')
def intent_fallback():
    speech_text = "Fallback intent"

    return question(speech_text)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555, debug=True)
