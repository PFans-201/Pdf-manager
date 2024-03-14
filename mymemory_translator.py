import requests

class MyMemoryTranslator:
    def translate(self, text, source_lang, target_lang):
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair={source_lang}|{target_lang}"
        response = requests.get(url)
        data = response.json()
        return data['responseData']['translatedText']
