import os
import json
import random
import sqlite3
import text_generator as tg


def generate_card_json(dog):
    # Default reply
    reply = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": tg.generate_card_utter(tg.TOPIC_UNKNOWN, None)
            },
            "card": {
                "type": "Standard",
                "title": "Dog Matcher",
                "text": tg.generate_card_utter(tg.TOPIC_UNKNOWN, None),
                "image": {
                    "smallImageUrl": "",
                    "largeImageUrl": ""
                }
            }
        }
    }

    if dog:
        dog_name = dog[1]
        dog_desc = dog[2].strip()
        dog_image = dog[9]

        # TODO use tg to generate text based on results
        reply["response"]["outputSpeech"]["text"] = tg.generate_card_utter(tg.TOPIC_CARD_SPEECH, dog)
        reply["response"]["card"]["title"] = dog_name
        reply["response"]["card"]["text"] = tg.generate_card_utter(tg.TOPIC_CARD_TEXT, dog)
        reply["response"]["card"]["image"]["smallImageUrl"] = dog_image
        reply["response"]["card"]["image"]["largeImageUrl"] = dog_image
    return reply


if __name__ == '__main__':
    # test
    DB_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../../dogs.db3'
    conn = sqlite3.connect(DB_PATH, isolation_level=None, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM %s WHERE %s < %s" % ('dogs', 'id', 6))
    dog = random.choice(cursor.fetchall())
    generate_card_json(dog)
