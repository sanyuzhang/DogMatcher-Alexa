import os
import json
import random
import sqlite3
from text_generator import *
from result_generator import elaborate_result
from config import *


def generate_card_json(dogs):
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
                "text": generate_card_utter(TOPIC_UNKNOWN, None),
                "image": {
                    "smallImageUrl": "",
                    "largeImageUrl": ""
                }
            }
        }
    }

    if dogs and len(dogs) > 0:
        # Randomly select one dog
        dog = random.choice(dogs)
        dog_name = dog[1]
        dog_image = dog[9]

        content = elaborate_result(dog)
        reply["response"]["outputSpeech"]["text"] = content
        reply["response"]["card"]["title"] = dog_name
        reply["response"]["card"]["text"] = content
        reply["response"]["card"]["image"]["smallImageUrl"] = dog_image
        reply["response"]["card"]["image"]["largeImageUrl"] = dog_image

    return reply


if __name__ == '__main__':
    # test
    conn = sqlite3.connect(DB_PATH, isolation_level=None, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM %s" % ('dogs'))
    dogs = cursor.fetchall()
    generate_card_json(dogs)
