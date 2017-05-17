import requests
import os


def add_feedback(feedback_type, field, value):
    try:
        response = requests.post(os.environ['feedback_url'], json={
            'type': feedback_type,
            field: value
        }, timeout=2)

        if response.status_code != 200:
            print(response.json())
    except Exception as ex:
        print(ex)
