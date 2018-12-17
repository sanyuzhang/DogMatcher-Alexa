import os
import json
import random
import sqlite3
from text_generator import *
from result_generator import elaborate_result
from config import *


def generate_card_json(dogs, top_n=5):
    # Default reply
    reply = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": generate_card_utter(TOPIC_UNKNOWN, None)
            },
            "card": {
                "type": "Standard",
                "title": "Dog Matcher",
                "text": generate_card_utter(TOPIC_UNKNOWN, None)
            }
        }
    }

    if dogs and len(dogs) > 0:
        if top_n > 1 and len(dogs) > 1:
            N = min(top_n, len(dogs))
            content = "We selected %s matched dogs for you. They are " % (N)
            for i in range(N):
                if i == N - 1:
                    content += dogs[i][1] + ". "
                elif i == N - 2:
                    content += dogs[i][1] + " and "
                else:
                    content += dogs[i][1] + ", "
            content += "You can ask me to tell more details about one of these dogs. Also, I can compare two dogs for you."
            reply["response"]["outputSpeech"]["text"] = content
            reply["response"]["card"]["text"] = content
        else:
            dog = random.choice(dogs)
            dog_name = dog[1]
            content = elaborate_result(dog)
            reply["response"]["outputSpeech"]["text"] = content
            reply["response"]["card"]["title"] = dog_name
            reply["response"]["card"]["text"] = content

    # print(reply)
    return reply


if __name__ == '__main__':
    # test
    conn = sqlite3.connect(DB_PATH, isolation_level=None, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM %s" % ('dogs'))
    dogs = cursor.fetchall()
    generate_card_json(dogs, top_n=3)
