import sqlite3
from text_generator import *
from result_generator import elaborate_result
from config import *


def generate_detail_json(dog):
    # More detail information about one dog

    # Default reply
    reply = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": generate_card_utter(TOPIC_UNKNOWN)
            },
            "card": {
                "type": "Standard",
                "title": "Dog Matcher",
                "text": generate_card_utter(TOPIC_UNKNOWN)
            },
            "shouldEndSession": False
        }
    }

    if dog:
        content = elaborate_result(dog)
        reply["response"]["outputSpeech"]["text"] = content
        reply["response"]["card"]["title"] = dog[1]
        reply["response"]["card"]["text"] = content

    # print(reply)
    return reply


def generate_card_json(dogs, top_n=5):
    # List all dogs we have found for the users

    # Default reply
    reply = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": generate_card_utter(TOPIC_UNKNOWN)
            },
            "card": {
                "type": "Standard",
                "title": "Dog Matcher",
                "text": generate_card_utter(TOPIC_UNKNOWN)
            },
            "shouldEndSession": False
        }
    }

    if dogs and len(dogs) > 0:
        if top_n > 1 and len(dogs) > 1:
            content, N = "", min(top_n, len(dogs))
            for i in range(N):
                if i == N - 1:
                    content += dogs[i][1] + ". "
                elif i == N - 2:
                    content += dogs[i][1] + " and "
                else:
                    content += dogs[i][1] + ", "
            content = generate_card_utter(TOPIC_CARD_COMPARE, top_n, content)
            reply["response"]["outputSpeech"]["text"] = content
            reply["response"]["card"]["text"] = content
        else:
            dog = random.choice(dogs)
            content = generate_card_utter(TOPIC_CARD_COMPARE, 1, dog[1])
            reply["response"]["outputSpeech"]["text"] = content
            reply["response"]["card"]["text"] = content

    # print(reply)
    return reply


if __name__ == '__main__':
    # for testing only
    conn = sqlite3.connect(DB_PATH, isolation_level=None, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM %s" % ('dogs'))
    dogs = cursor.fetchall()
    generate_card_json(dogs, top_n=1)
    generate_card_json(dogs, top_n=5)

    cursor.execute("SELECT * FROM %s" % ('dogs'))
    dog = cursor.fetchone()
    generate_detail_json(dog)
