from deep_translator import GoogleTranslator

# Переводчик на русский с любого языка (source='auto' - с любого языка, target='ru' - на русский)
def translate(text):
    translator = GoogleTranslator(source='auto', target='ru')
    translated_text = translator.translate(text)
    print(translated_text)
    return translated_text

def translate_to_en(text):
    translator = GoogleTranslator(source='auto', target='en')
    translated_text = translator.translate(text)
    print(translated_text)
    return translated_text


