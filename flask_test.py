import logging
from flask import Flask, request, render_template

from flask_ask import Ask, statement, question

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

topic=''

#@app.route("/", methods=["POST", "GET")
def hello():
    data = (request.get_json(silent=True))['request']['intent']
    print(data)


@ask.launch
def launch():
    speech_text = 'Welcome to the Alexa Skills Kit, you can say hello,gr'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)

@ask.intent('Portal')
def IntentPortal(game):
    return statement(game).simple_card('HelloWorld', game)

@ask.intent('GetNewFactIntent')
def IntentGetNewFact():
    return question("No fact for you").simple_card('Fact', 'No fact lol')

@ask.intent('PronounIntent',mapping={'color':'color','breed':'breed','pronoun':'pronoun'})
def IntentPronoun(color, pronoun,breed):
    if color!='' or breed != '':
        #inquire database
        #print(pronoun)
        msg="By saying  "+str(pronoun)+", do you mean "+breed
        return question(msg)
    else:
        return question("No fact for you").simple_card('Fact', 'No fact lol')

@ask.intent('ReferenceIntent',mapping={'breed':'breed'})
def IntentReference(breed):
    print(breed)
    msg = "Good, you like "+ breed
    return question(msg).simple_card('Fact', 'No fact lol')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5557, debug=True)

