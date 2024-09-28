import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/bugfixer/p1', methods=['POST'])
def expose():

    data = request.get_json()

    resultant_list = []
    for project in data:

        times = project.get('time')
        prereqs = project.get('prerequisites')

        proj_timing_dict = {}

        for index in range(len(times)):
            proj_timing_dict[index+1] = [times[index], 0]

        for prereq in prereqs:
            dep = prereq[1]
            indep = prereq[0]

            if proj_timing_dict[indep][0] > proj_timing_dict[dep][1]:
                proj_timing_dict[dep][0] = proj_timing_dict[dep][0] - proj_timing_dict[dep][1] + proj_timing_dict[indep][0]
                proj_timing_dict[dep][1] = proj_timing_dict[indep][0]

        # get the highest timing
        key_with_highest_value = max(proj_timing_dict, key=lambda k: proj_timing_dict[k][0])
        highest_value = proj_timing_dict[key_with_highest_value][0]
        resultant_list.append(highest_value)
        
    return json.dumps(resultant_list)
