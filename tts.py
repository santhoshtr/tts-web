import json
import os

from TTS.api import TTS

from lid import LanguageIdentification

lid = LanguageIdentification()

current_dir = os.path.dirname(os.path.abspath(__file__))
models = json.load(open(os.path.join(current_dir, "models.json")))


def text_to_speech_file(text: str, language):
    mms_code = ""
    if not language or language == "auto":
        lang_prediction = lid.predict(text)
        language = lang_prediction.get("wikicode")
        mms_code = lang_prediction.get("alpha3")

    print("Predicted language", language)
    if language not in models:
        model_name = f"tts_models/{mms_code}/fairseq/vits"
    else:
        model_name = models.get(language)
    api = TTS(model_name=model_name)
    return api.tts_to_file(text)
