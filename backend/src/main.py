# Backend for DogMatcher alexa skill

import logging

from flask import Flask, make_response, jsonify
from flask_ask import Ask, question, session
from text_generator import generate_clarification, generate_utter
from result_generator import elaborate_result
from card_generator import generate_card_json
from query import query
from config import *

app = Flask(__name__)
ask = Ask(app, "/")
log = logging.getLogger('flask_ask').setLevel(logging.DEBUG)

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


def update_dog_parameter(value):
    # record answer
    # first, find out which question is user answering
    prev_state = get_state()

    # second, find out what parameter does that question leads to
    if prev_state not in QUESTION_PARAMETER:
        return
    parameter = QUESTION_PARAMETER[prev_state]

    # finally, store new value to this parameter
    set_dog_parameter(parameter, value)


def advance_state(ans):
    # change state
    prev_state = get_state()
    directions = DIRECTION_QUESTIONS[prev_state]

    # get next state
    if type(directions) == int:
        next_state = directions
    else:
        next_state = directions[ans]

    set_state(next_state)
    return get_state()


def answer_question(ans):
    # store user answer
    update_dog_parameter(ans)

    # check if end of question
    if get_state() == END_OF_QUESTION:
        return all_question_answered()

    # change state
    advance_state(ans)

    # get next question
    speech_text = generate_utter(get_state())

    return question(speech_text).reprompt(speech_text)


def query_base_on_user_para():
    def clamp(val_min, val_max, val):
        return min(val_max, max(val_min, val))

    para = get_session_attr(ATTRIBUTE_DOG_PARAMETER)

    # int
    train_time = clamp(1, 1000, int(para["trainTime"]))
    # bool
    apt_dog = bool(para["aptDog"])
    # int
    bark_level = clamp(1, 5, int(para["barkLevel"]))
    # int
    shed_level = clamp(1, 5, int(para["shedLevel"]))
    # bool
    have_kids = bool(para["haveKids"])
    # int
    activity_level = clamp(1, 4, int(para["activityLevel"]))

    return query(train_time, apt_dog, bark_level, shed_level, have_kids, activity_level)


def all_question_answered():
    # make query
    dogs = query_base_on_user_para()

    num = min(5, len(dogs))

    reply = generate_card_json(dogs, top_n=num)
    reply["sessionAttributes"] = session.attributes
    return make_response(jsonify(reply))


'''
ASK Intent Entries
'''


@ask.on_session_started
def new_session():
    log.info('Dog Matcher skill new session started')


@ask.launch
def launch():
    # init state
    set_state(1)

    # init parameters for later SQL query
    set_session_attr(ATTRIBUTE_DOG_PARAMETER, DEFAULT_PARAMETER)

    speech_text = generate_utter(0)
    speech_text += generate_utter(1)

    reprompt = speech_text

    return question(speech_text).reprompt(reprompt)


@ask.intent('confirm')
def intent_confirm():
    return answer_question(True)


@ask.intent('deny')
def intent_deny():
    return answer_question(False)


@ask.intent('numeric')
def intent_numeric(slot_number):
    # For the activity level, 1 is the most active and 4 is the most inactive
    if get_state() == 8:
        slot_number = 5 - slot_number

    return answer_question(slot_number)


@ask.intent('ans_home_type')
def intent_ans_home_type(slot_home):
    val = {
        "apt": True,
        "house": False
    }[slot_home]

    return answer_question(val)


@ask.intent('ans_train_time_week')
def intent_ans_train_time_week(slot_number):
    return answer_question(slot_number)


@ask.intent('ans_exp_level')
def intent_ans_exp_level(slot_exp_level):
    val = {
        "yes": True,
        "no": False
    }[slot_exp_level]

    return answer_question(val)


@ask.intent('ans_barking_level')
def intent_ans_barking_level(slot_barking_level):
    """
    User answers barking level

    :param slot_barking_level: a str representation of integer from 1 to 5
    :type slot_barking_level: str
    """
    val = int(slot_barking_level)

    return answer_question(val)


@ask.intent('ans_shed_level')
def intent_ans_shed_level(slot_shed_level):
    """
    User answers Shedding level
    """
    val = int(slot_shed_level)

    return answer_question(val)


@ask.intent('ans_activity_level')
def intent_ans_activity_level(slot_activity_level):
    """
    User answers activity level
    """
    val = int(slot_activity_level)

    return answer_question(val)


@ask.intent('AMAZON.FallbackIntent')
def intent_fallback():
    # speech_text = "Fallback intent"

    # return question(speech_text)
    # init state
    set_state(1)

    # init parameters for later SQL query
    set_session_attr(ATTRIBUTE_DOG_PARAMETER, DEFAULT_PARAMETER)

    # speech_text = generate_utter(0)
    speech_text = generate_utter(1)

    reprompt = speech_text

    return question(speech_text).reprompt(reprompt)


@ask.intent('clarification')
def intent_clarification():
    speech_text = generate_clarification(int(get_state()))

    return question(speech_text)

@ask.intent('breed_compare')
def intent_breed_compare(slot_ordinal_c,slot_ordinal_cc):
    result = query_base_on_user_para()
    ORDINALS = ["first", "second", "third", "forth", "fifth", "sixth", "seventh","eighth","ninth","tenth"]
    if len(result) <= 1:
        speech_text = "Nothing to compare."
    elif (ORDINALS.index(slot_ordinal_c) < len(result)) and (ORDINALS.index(slot_ordinal_cc) < len(result)):
        speech_text = compareDogRows(result[ORDINALS.index(slot_ordinal_c)], result[ORDINALS.index(slot_ordinal_cc)])
    else:
        speech_text = compareDogRows(result[-2], result[-1])
    return question(speech_text)


@ask.intent('info_request')
def intent_info_request(slot_breed, slot_pronoun, slot_ordinal):
    ORDINALS = ["first", "second", "third", "forth", "fifth", "sixth", "seventh","eighth","ninth","tenth"]
    result = query_base_on_user_para()

    speech_text = ""

    if slot_breed is not None:
        new_result = [idog for idog in result if idog[1] == slot_breed]
        speech_text = generate_detail_json(new_result[0])
    elif slot_ordinal is None:
        speech_text = generate_detail_json(result[0])
    elif slot_ordinal is not None:
        if ORDINALS.index(slot_ordinal) >= len(result):
            speech_text = generate_detail_json(result[-1])
        else:
            speech_text = generate_detail_json(result[ORDINALS.index(slot_ordinal)])

    return question(speech_text)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555, debug=True)
