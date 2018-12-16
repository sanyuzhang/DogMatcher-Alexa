# Backend for DogMatcher alexa skill

"""
todo: import text_generator.py
"""

import logging

from flask import Flask
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")
log = logging.getLogger('flask_ask').setLevel(logging.DEBUG)

ELICIT_QUESTIONS = {
    0: "Welcome to the Dog Matcher skill, I will help you find your dream dog by asking some questions. Let's begin with one simple question. ",
    2: "How much time can you put into training your dog every day?",
    3: "What is your home like? Is it an apartment or a house with yard?",
    4: "Do you want to look for dogs for apartment environment only?",
    5: "From a scale of 1 to 10, how well can you stand for barking or noise made by dogs?",
    6: "From a scale of 1 to 10, how well can you stand for shedding?",
    7: "Do you live with kids under 10?",
    8: "From a scale of 1 to 10, how active do you want the dog be?"
}

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
    8: []
}


def get_session_attr(attr):
    return session.attributes[attr]


def set_session_attr(key, value):
    session.attributes[key] = value


def set_state(state):
    set_session_attr("state", state)


def get_state():
    return get_session_attr("state")


# todo: record user's answer


def user_answer_binary_question(ans):
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
    # change state
    prev_state = get_state()
    next_state = DIRECTION_QUESTIONS[prev_state]
    set_state(next_state)

    # get next question
    speech_text = generate_utter(get_state())

    return question(speech_text).reprompt(speech_text)


"""
ASK Intent Entries
"""


@ask.on_session_started
def new_session():
    log.info('Dog Matcher skill new session started')


# @app.route("/", methods=["POST", "GET"])
@ask.launch
def launch():
    set_state(1)

    speech_text = ELICIT_QUESTIONS[0] + generate_utter(TOPIC_EXP_ID)

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
