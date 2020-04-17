from googletrans import Translator

__all__ = ["translate"]


def translate(text, lang):
    """
    Translate text to the provided language

    :param text: original text
    :param lang: destination language
    :return: Translated text
    """
    translator = Translator()
    return translator.translate(text, dest=lang).text