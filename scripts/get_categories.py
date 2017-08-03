import os
import requests
import scripts.alexa_response as alexa_response


def on_intent(event, intent_name):

    response = get_api_response()
    print(response.url)
    print(response.json())

    categories = response.json()
    # categories = list(map(lambda x: x['card_name'], categories))

    return generate_alexa_response(response.status_code, categories, intent_name)


def get_api_response():
    url = os.environ['get_categories_url']
    return requests.get(url)


def generate_alexa_response(status_code, categories, intent_name):
    if status_code == 200 and len(categories) != 0:
        speech = "<speak>We currently have " + str(len(categories)) + ' categories' \
                 + " <break time='2s' />"
        for category in categories:
            speech += category + "<break time='1s' />"
        speech += "</speak>"
        card_text = '\n'.join(categories)
        return alexa_response.generate_alexa_response(speech, 'SSML', intent_name, card_text, 'Simple')
    else:
        return alexa_response.generate_internal_error_response()

if __name__ == "__main__":
    os.environ['get_categories_url'] = 'https://m8n05huk4i.execute-api.us-east-1.amazonaws.com/dev/categories'
    print(on_intent(None, 'MyCardsIntent'))
