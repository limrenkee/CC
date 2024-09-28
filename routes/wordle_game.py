import logging
import json
from flask import request
from routes import app

logger = logging.getLogger(__name__)


@app.route('/wordle-game', methods=['POST'])
def expose():

    with open("data/wordle-list.txt", "r") as file: 
        allText = file.read() 
        words = list(map(str, allText.split())) 
    
    # get request data
    logging.info(request.get_json())
    guess_feedback = request.get_json()
    guessHistory = guess_feedback.get('guessHistory')
    evaluationHistory = guess_feedback.get('evaluationHistory')

    logging.info(guessHistory)
    logging.info(evaluationHistory)


    for history_index in range(len(evaluationHistory)):
        logging.info("MOVING TO NEXT HISTORY")
        for eval_index in range(len(evaluationHistory[history_index])):
            filtered_list = []
            # correct letter correct position
            if evaluationHistory[history_index][eval_index] == "X":
                for word in words:
                    if guessHistory[history_index][eval_index] in word:
                        filtered_list.append(word)

            # no such character
            elif evaluationHistory[history_index][eval_index] == "-":
                for word in words:
                    if guessHistory[history_index][eval_index] not in word:
                        filtered_list.append(word)

            elif evaluationHistory[history_index][eval_index] == "O":
                for word in words:
                    if word[eval_index] == guessHistory[history_index][eval_index]:
                        filtered_list.append(word)
            else:
                continue

            words = filtered_list

    return json.dumps({"guess": words[0]})
    




