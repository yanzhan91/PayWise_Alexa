def generate_alexa_response(speech, speech_type, card_title, card_text, card_type='Simple', reprompt_speech='',
                            reprompt_type='PlainText', end_session=True):
    output_speech = generate_output_speech(speech, speech_type)
    card = generate_card(card_title, card_text, card_type)
    reprompt = generate_reprompt(reprompt_speech, reprompt_type)
    return generate_response(card, output_speech, reprompt, end_session)


def generate_internal_error_response():
    speech = 'There\'s an internal error. Please try again later'
    card_title = 'Error with Skill'
    return generate_alexa_response(speech, 'PlainText', card_title, speech, 'Simple')


def generate_response(card, output_speech, reprompt, should_end_session):
    response = {
        'version': '1.0',
        'response': {
            'outputSpeech': output_speech,
            'card': card,
            'reprompt': reprompt,
            'shouldEndSession': should_end_session
        },
        'sessionAttributes': {}
    }
    return response


def generate_reprompt(speech, speech_type):
    return {
        'outputSpeech': generate_output_speech(speech, speech_type)
    }


def generate_card(card_title, speech, card_type):
    return {
        'content': speech,
        'title': card_title,
        'type': card_type
    }


def generate_output_speech(speech, speech_type):
    return {
        'type': speech_type,
        'ssml': speech,
        'text': speech
    }

