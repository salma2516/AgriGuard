from googletrans import Translator

translator = Translator()

def translate_text(
    text,
    language
):

    try:

        return translator.translate(
            text,
            dest=language
        ).text

    except:

        return text