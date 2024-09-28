import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/klotski', methods=['POST'])
def evaluate():

    data = request.get_json()

    resultant_list = []
    for board_list in data:

        logging.info("data sent for evaluation {}".format(data))

        board = board_list.get('board')
        moves = board_list.get('moves')

        board_list = list(board)

        move_steps = [moves[i:i+2] for i in range(0, len(moves), 2)]

        move_dict = {}
        for move in move_steps:
            block = move[0]
            direction = move[1]

            if direction == "N":
                if block in move_dict: 
                    move_dict[block] -= 4
                else:
                    move_dict[block] = -4

            elif direction == "E":
                if block in move_dict: 
                    move_dict[block] += 1
                else:
                    move_dict[block] = 1

            elif direction == "S":
                if block in move_dict: 
                    move_dict[block] += 4
                else:
                    move_dict[block] = 4

            elif direction == "W":
                if block in move_dict: 
                    move_dict[block] -= 1
                else:
                    move_dict[block] = -1

        all_old = []
        all_new = []

        for block,move_value in move_dict.items():
    
            old_block_indexes = [index for index, c in enumerate(board) if c == block]
            all_old += old_block_indexes

            new_block_indexes = [index + move_value for index in old_block_indexes]
            all_new += new_block_indexes

            for index in new_block_indexes:

                board_list[index] = block

        difference = list(set(all_old) - set(all_new))
        for index in difference:
            board_list[index] = "@"

        resultant_list.append("".join(board_list))

    return json.dumps(resultant_list)
