import os
import requests
import scripts.alexa_response as alexa_response


def on_intent(event, intent_name, operation):
    user_id = event['session']['user']['userId']
    slots = event['request']['intent']['slots']

    if 'Card' not in slots or 'value' not in slots['Card']:
        return generate_alexa_response(400, None, None, None)

    card_name = slots['Card']['value']

    # TODO Temporary Fix for Quicksilver and Quicksilver One issue
    if card_name == 'capital 1 quicksilver 1':
        card_name = 'capital one quicksilver one'

    response = get_api_response(user_id, card_name, operation)
    print(response.url)
    print(response.json())

    if response.status_code == 200:
        card_name = response.json()

    return generate_alexa_response(response.status_code, card_name, intent_name, operation)


def get_api_response(user_id, card_name, operation):
    url = os.environ['user_card_url']

    if operation == 'add':
        return requests.post(url, json={
            'user_id': user_id,
            'card_name': card_name,
            'device': 'Alexa'
        })
    elif operation == 'delete':
        url += '?device=Alexa&user_id=' + user_id + '&card_name=' + card_name
        return requests.delete(url)
    else:
        alexa_response.generate_internal_error_response()


def generate_alexa_response(status_code, card_name, intent_name, operation):
    if status_code == 200:
        if operation == 'add':
            speech = card_name + ' has been added successfully'
        else:
            speech = card_name + ' has been deleted successfully'
        return alexa_response.generate_alexa_response(speech, 'PlainText', intent_name, speech, 'Simple')
    elif status_code == 400:
        speech = card_name + ' currently does not exist in our database.'
        return alexa_response.generate_alexa_response(speech, 'PlainText', intent_name, speech, 'Simple')
    else:
        return alexa_response.generate_internal_error_response()


if __name__ == "__main__":

    os.environ['user_card_url'] = 'https://m8n05huk4i.execute-api.us-east-1.amazonaws.com/dev/user-cards'
    mock_event = {
        'request': {
            'intent': {
                'name': 'SetCardIntent',
                'slots': {
                    'Card': {
                        'value': 'Chase Fdom'
                    }
                }
            }
        },
        'session': {
            'user': {
                'userId': '10005'
            }
        }
    }
    print(on_intent(mock_event, 'SetCardIntent', 'add'))
