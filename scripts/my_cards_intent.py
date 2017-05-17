import os
import requests
import scripts.alexa_response as alexa_response


def on_intent(event, intent_name):
    user_id = event['session']['user']['userId']

    response = get_api_response(user_id)
    print(response.url)
    print(response.json())

    cards = response.json()
    cards = list(map(lambda x: x['card_name'], cards))

    return generate_alexa_response(response.status_code, cards, intent_name)


def get_api_response(user_id):
    url = os.environ['get_user_cards_url'] + '?user_id=' + user_id
    return requests.get(url)


def generate_alexa_response(status_code, cards, intent_name):
    if status_code == 200 and len(cards) != 0:
        speech = "<speak>You have " + str(len(cards)) + (' cards' if len(cards) > 0 else ' card') \
                 + " cards added.<break time='2s' />"
        for card in cards:
            speech += card + "<break time='1s' />"
        speech += "</speak>"
        card_text = '\n'.join(cards)
        return alexa_response.generate_alexa_response(speech, 'SSML', intent_name, card_text, 'Simple')
    elif status_code == 400 or len(cards) == 0:
        speech = 'You have not saved any cards yet. '
        reprompt_speech = 'To add a card, simply say add, followed by a card name such as chase freedom.'
        return alexa_response.generate_alexa_response(speech + reprompt_speech, 'PlainText', intent_name, speech,
                                                      'Simple', reprompt_speech, 'PlainText', False)
    else:
        return alexa_response.generate_internal_error_response()

if __name__ == "__main__":
    os.environ['get_user_cards_url'] = 'https://m8n05huk4i.execute-api.us-east-1.amazonaws.com/dev/user-cards'
    mock_event = {
        'request': {
            'intent': {
                'name': 'MyCardsIntent',
                'slots': {}
            }
        },
        'session': {
            'user': {
                'userId': '10001'
            }
        }
    }
    print(on_intent(mock_event, 'MyCardsIntent'))
