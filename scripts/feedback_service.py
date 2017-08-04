import requests
import os


def add_feedback(feedback_type, field, value):
    try:
        url = os.environ['base_url'] + os.environ['env'] + os.environ['feedback_url']
        response = requests.post(url, json={
            'type': feedback_type,
            field: value
        }, timeout=2)

        if response.status_code != 200:
            print(response.json())
    except Exception as ex:
        print(ex)
