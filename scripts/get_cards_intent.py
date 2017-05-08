import os
import requests
import scripts.alexa_response as alexa_response
from decimal import Decimal


def on_intent(event, intent_name):

    user_id = event['session']['user']['userId']
    slots = event['request']['intent']['slots']

    name = None
    category = None

    if 'Name' in slots:
        name = slots['Name']['value']
    if 'Category' in slots:
        category = slots['Category']['value']

    url = build_url(os.environ['get_rewards_url'], str(user_id), name, category)
    print(url)

    api_response = get_api_response(url)
    print(api_response.status_code)
    print(api_response.json())

    return generate_alexa_response(api_response, intent_name)


def build_url(url, user_id, name, category):
    url = url + '?device=Alexa&user_id=' + user_id
    if name is not None:
        url = url + '&name=' + name.replace(' ', '%20')
    if category is not None:
        url = url + '&category=' + category
    return url


def get_api_response(url):
    return requests.get(url)


def generate_speech(results):
    speech = '<speak>'
    if not results:
        speech = 'You do not have any cards saved.'
    else:
        del results[3:]
        for card_info in results:
            percentage = float(card_info['reward'])
            percentage = str(Decimal(percentage).normalize())
            speech += (card_info['card_name'] + ' will give you ' + percentage + " percent <break time='1s' />")
    speech += '</speak>'
    return speech


def generate_alexa_response(api_response, intent_name):
    if api_response.status_code == 200:
        return get_response_for_200(api_response, intent_name)
    elif api_response.status_code == 400:
        return get_response_for_400()
    else:
        return get_response_for_500()


def get_response_for_200(api_response, intent_name):
    results = api_response.json()
    speech = generate_speech(results)
    return alexa_response.generate_alexa_response(speech, 'SSML', intent_name, '', 'Simple')


def get_response_for_400():
    return alexa_response.generate_alexa_response('')


def get_response_for_500():
    return alexa_response.generate_internal_error_response()

if __name__ == "__main__":

    os.environ['get_rewards_url'] = 'https://m8n05huk4i.execute-api.us-east-1.amazonaws.com/dev/rewards'
    mock_event = {
        'request': {
            'intent': {
                'name': 'GetCardsIntent',
                'slots': {
                    'Name': {
                        'value': 'sdfsdf'
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
    print(on_intent(mock_event, 'GetCardsIntent'))
