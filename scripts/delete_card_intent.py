import os
import requests
import scripts.alexa_response as alexa_response


# Deprecated
def on_intent(event, intent_name):
    user_id = event['session']['user']['userId']
    slots = event['request']['intent']['slots']

    if 'Card' not in slots or 'value' not in slots['Card']:
        return generate_alexa_response(400, None, None)

    card_name = slots['card']['value']

    response = get_api_response(user_id, card_name)
    print(response.url)
    print(response.json())

    if response.status_code == 200:
        card_name = response.json()

    return generate_alexa_response(response.status_code, card_name, intent_name)


def get_api_response(user_id, card_name):
    url = os.environ['user_card_url']
    url += '?device=Alexa&user_id=' + user_id + '&card_name=' + card_name
    return requests.delete(url)


def generate_alexa_response(status_code, card_name, intent_name):
    if status_code == 200:
        speech = card_name + ' has been successfully deleted'
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
                'slots': {
                    'Card': {
                        'value': 'Chase Freedom'
                    }
                }
            }
        },
        'session': {
            'user': {
                'userId': '10001'
            }
        }
    }
    print(on_intent(mock_event, 'DeleteCardIntent'))
