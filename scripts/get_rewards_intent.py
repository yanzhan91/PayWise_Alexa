import os
import requests
import scripts.alexa_response as alexa_response
import scripts.feedback_service as feedback_service
from decimal import Decimal


def on_intent(event, intent_name):

    user_id = event['session']['user']['userId']
    slots = event['request']['intent']['slots']

    name = None
    category = None

    if 'Name' in slots:
        name = slots['Name']['value']
    elif 'category' in slots:
        category = slots['category']['value']
    else:
        speech = 'Please try again with a category such as restaurants'
        alexa_response.generate_alexa_response(speech, 'PlainText', intent_name, speech, 'Simple')

    url = build_url(str(user_id), name, category)
    print(url)

    api_response = requests.get(url)
    print(api_response.status_code)
    print(api_response.json())

    return generate_alexa_response(api_response, intent_name, name, category)


def build_url(user_id, name, category):
    url = os.environ['base_url'] + os.environ['env'] + os.environ['get_rewards_url'] \
          + '?device=Alexa&user_id=' + user_id
    if name is not None:
        url = url + '&name=' + name.replace(' ', '%20')
    if category is not None:
        url = url + '&category=' + category
    return url


def generate_alexa_response(api_response, intent_name, name, category):
    if api_response.status_code == 200:
        results = api_response.json()
        if not results:
            speech = 'You have not saved any cards yet. '
            reprompt_speech = 'To add a card, simply say add, followed by a card name such as chase freedom.'
            return alexa_response.generate_alexa_response(speech + reprompt_speech, 'PlainText', intent_name, speech,
                                                          'Simple', reprompt_speech, 'PlainText', False)
        speech, card_text = generate_speech(results, category)
        return alexa_response.generate_alexa_response(speech, 'SSML', intent_name, card_text, 'Simple')
    elif api_response.status_code == 400:
        if name:
            user_input = name
            feedback_service.add_feedback('store', 'store', user_input)
        elif category:
            user_input = category
            feedback_service.add_feedback('category', 'category', user_input)
        else:
            return alexa_response.generate_internal_error_response()

        speech = user_input + ' currently does not exist in our database. Check back later as we continuously add ' \
                              'new ones everyday'
        return alexa_response.generate_alexa_response(speech, 'PlainText', intent_name, speech, 'Simple')
    else:
        return alexa_response.generate_internal_error_response()


def generate_speech(results, category):
    speech = '<speak>'
    card_text = category + '\n'
    del results[3:]
    for card_info in results:
        percentage = float(card_info['reward'])
        percentage = str(Decimal(percentage).normalize())
        speech += (card_info['card_name'] + ' will give you ' + percentage + " percent <break time='1s' />")
        card_text += (card_info['card_name'] + ' - ' + percentage + '%')
    speech += '</speak>'
    return speech, card_text


if __name__ == "__main__":
    os.environ['base_url'] = 'https://m8n05huk4i.execute-api.us-east-1.amazonaws.com/'
    os.environ['env'] = 'dev'
    os.environ['get_rewards_url'] = '/rewards'
    mock_event = {
        'request': {
            'intent': {
                'name': 'GetRewardsIntent',
                'slots': {
                    'category': {
                        'value': 'movie'
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
