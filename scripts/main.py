import scripts.get_cards_intent as get_cards_intent
import scripts.set_delete_card_intent as set_delete_card_intent
import scripts.my_cards_intent as my_cards_intent
import scripts.alexa_response as alexa_response


def handler(event, context):
    print(event)
    response = start_request(event)
    print(response)
    return response


def start_request(event):
    intent_name = event['request']['intent']['name']
    if intent_name == 'GetCardsIntent':
        return get_cards_intent.on_intent(event, intent_name)
    elif intent_name == 'SetCardIntent':
        return set_delete_card_intent.on_intent(event, intent_name, 'add')
    elif intent_name == 'DeleteCardIntent':
        return set_delete_card_intent.on_intent(event, intent_name, 'delete')
    elif intent_name == 'MyCardsIntent':
        return my_cards_intent.on_intent(event, intent_name)
    else:
        return alexa_response.generate_internal_error_response()
