import json
import logging
from itertools import combinations

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/bugfixer/p2', methods=['POST'])
def expose():

    data = request.get_json()

    resultant_list = []
    for project in data:

        bugseq = project.get('bugseq')
        indexed_elements = [(sublist[0], index) for index, sublist in enumerate(bugseq)]
        subsets = []
        for r in range(len(indexed_elements) + 1):  # r goes from 0 to len(nums)
            subsets.extend(combinations(indexed_elements, r))  # Generate all combinations of length r

        max_item = 0
        for subset in reversed(subsets):

            max_capacity = 0

            for items in subset:
                index = items[1]
                capacity = bugseq[index][1]
                if capacity > max_capacity:
                    max_capacity = capacity

            if max_capacity >= sum(item[0] for item in subset) and len(subset) > max_item:
                max_item = len(subset)

        resultant_list.append(max_item)  
        
    return json.dumps(resultant_list)
