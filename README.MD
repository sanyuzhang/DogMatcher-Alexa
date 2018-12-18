# DogMatcher

A interactive system that helps user find the most suitable dog breed based on user’s life habits

Team member: Zijie Wu, Guirong Liu, Shangyu Zhang, Anyan Xie

Links:
* [Presentation](https://docs.google.com/presentation/d/1QjM9lr_FkqYJaXlHvrHAILrnm93DXM9eHZcHu7-WS4M/edit?usp=sharing)

## Design

This project involves 2 parts: Alexa skill and a backend.

The Alexa Skill will parse users' utterances, then trigger correct intent, which will then handled by backend, generating proper response.

### Project Flowchart

![picture not found](https://i.ibb.co/RHnWJkG/Screen-Shot-2018-12-15-at-14-46-12.png)

## How to use

This project involves 2 parts: Alexa Skill and a backend

### Backend Setups

#### Install Dependency

```bash
# install virtualenv to easily manage python versions
pip install virtualenv 

# Create your own ENV like
virtualenv ENV

# Source your ENV
source ENV\bin\activate

# Install packages by typing
pip install -r requirements.txt
```

#### Run

To run backend:
1. Enable the correct python virtual env
2. `python backend/src/main.py`

A flask server will run on port 5555.

### Alexa Skill setup

1. Create an Alexa Skill and copy `alexa_skill.json` into the JSON editor.
2. Set the endpoint to the Flask server.
3. Build and run skill.


