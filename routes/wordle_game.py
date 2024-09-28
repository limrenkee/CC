import logging
import json
from flask import request
from routes import app
import math
import itertools
import string

logger = logging.getLogger(__name__)


@app.route('/wordle-game', methods=['POST'])
def expose():

    with open("data/words.txt", "r") as file: 
        allText = file.read() 
        words = list(filter(lambda word: len(word) == 5, allText.split())) 
    
    # get request data
    logging.info(request.get_json())
    guess_feedback = request.get_json()
    guessHistory = guess_feedback.get('guessHistory')
    evaluationHistory = guess_feedback.get('evaluationHistory')

    logging.info(guessHistory)
    logging.info(evaluationHistory)

    if evaluationHistory == []:
        return json.dumps({"guess": "slate"})

    for history_index in range(len(evaluationHistory)):
        words.remove(guessHistory[history_index])
        logging.info("MOVING TO NEXT HISTORY")
        for eval_index in range(len(evaluationHistory[history_index])):
            filtered_list = []
            # correct letter wrong position
            if evaluationHistory[history_index][eval_index] == "X":
                for word in words:
                    if (guessHistory[history_index][eval_index] in word) and (word[eval_index] != guessHistory[history_index][eval_index]):
                        filtered_list.append(word)

            # no such character
            elif evaluationHistory[history_index][eval_index] == "-":
                for word in words:
                    if (guessHistory[history_index][eval_index] not in word[:eval_index]) or (guessHistory[history_index][eval_index] not in word[eval_index+1:]):
                        filtered_list.append(word)

            # correct letter correct position
            elif evaluationHistory[history_index][eval_index] == "O":
                for word in words:
                    if word[eval_index] == guessHistory[history_index][eval_index]:
                        filtered_list.append(word)
            else:
                continue

            words = filtered_list
            # logging.info(words)

            if len(words) == 0:
                logging.info('did not managed to find a word in my word list')
                return json.dumps({"guess": "aback"})

    logging.info("final word list {}".format(words))
    return json.dumps({"guess": words[0]})
    




