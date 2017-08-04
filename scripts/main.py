import scripts.get_rewards_intent as get_rewards_intent
import scripts.set_delete_card_intent as set_delete_card_intent
import scripts.my_cards_intent as my_cards_intent
import scripts.alexa_response as alexa_response
import scripts.get_categories as get_categories


def handler(event, context):
    print(event)
    response = start_request(event)
    print(response)
    return response


def start_request(event):
    if 'intent' not in event['request']:
        return handle_help_response()
    intent_name = event['request']['intent']['name']
    if intent_name == 'GetRewardsIntent':
        return get_rewards_intent.on_intent(event, intent_name)
    elif intent_name == 'SetCardIntent':
        return set_delete_card_intent.on_intent(event, intent_name, 'add')
    elif intent_name == 'DeleteCardIntent':
        return set_delete_card_intent.on_intent(event, intent_name, 'delete')
    elif intent_name == 'MyCardsIntent':
        return my_cards_intent.on_intent(event, intent_name)
    elif intent_name == 'AllCategoriesIntent':
        return get_categories.on_intent(event, intent_name)
    elif intent_name == 'AMAZON.CancelIntent' or intent_name == 'AMAZON.StopIntent':
        return handle_empty_response()
    elif intent_name == 'AMAZON.HelpIntent':
        return handle_help_response()
    else:
        return alexa_response.generate_internal_error_response()


def handle_empty_response():
    return {
        'version': '1.0',
        'response': {
            'shouldEndSession': True
        }
    }


def handle_help_response():
    speech = 'Welcome to Pay Wise. A service to help you maximize your credit card rewards. ' \
             'To start, add your credit cards by simply saying add, followed by the card name. For example, add ' \
             'Chase Freedom. Then you can ask me about a category. To find our current list of categories, ' \
             'simply say, all categories'
    return alexa_response.generate_alexa_response(speech, 'PlainText', 'PayWise Help', speech, end_session=False)
