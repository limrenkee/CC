import logging
import json
from flask import request
from routes import app
from datetime import datetime
import pytz
# from pytz import timezone

logger = logging.getLogger(__name__)

# Helper function to parse and convert time to UTC
def convert_to_utc(time_str):
    # Parse the ISO time string into a datetime object
    dt = datetime.fromisoformat(time_str)
    # Convert it to UTC
    return dt.astimezone(pytz.utc)


@app.route('/mailtime', methods=['POST'])
def expose():

    # get request data
    logging.info(request.get_json())
    data = request.get_json()
    emails = data.get('emails')
    users = data.get('users')


    data_sorted = sorted(emails, key=lambda x: convert_to_utc(x['timeSent']))
    unique_threads = {}
    for email in emails:
        # get unique email thread
        if "RE: " not in email['subject']:
            unique_threads[email['subject']] = []

    for email in emails:
        for subject in unique_threads.keys():
            if subject in email['subject']:
                unique_threads[subject].append(email)

    response_time_dict = {}
    for subject, emails in unique_threads.items():
        for email in emails:
            if email['subject'] == subject:
                send_time = convert_to_utc(email['timeSent'])
            else:
                logging.info("i am in HEREE-----------------------")
                response_time = (convert_to_utc(email['timeSent']) - send_time).total_seconds()
                if email['sender'] in response_time_dict:
                    response_time_dict[email['sender']][0] += response_time
                    response_time_dict[email['sender']][1] += 1
                else:
                    response_time_dict[email['sender']] = [response_time,1]

                send_time = convert_to_utc(email['timeSent'])

    logging.info(response_time_dict.items())
    for key,value in response_time_dict.items():
        response_time_dict[key] = value[0]/value[1]
    # logging.info(unique_threads)


    return json.dumps({"responses": response_time_dict})
    




