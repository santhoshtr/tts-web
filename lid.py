import csv
import logging
import os
from typing import Dict

import fasttext

current_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(current_dir, "models")
model_path = os.path.join(models_dir, "lid201-model.bin")


class LanguageIdentification:
    def __init__(self):
        self.ready = False
        self.languages: Dict[str, str] = self.create_language_lookup()
        self.alpha2_3_languages: Dict[str, str] = self.create_iso_lookup()
        self.load()

    def create_language_lookup(self) -> Dict[str, str]:
        csv_path = os.path.join(current_dir, "languages-isotowiki.tsv")
        csv_reader = csv.DictReader(open(csv_path), delimiter="\t")
        languages: Dict[str, str] = {}
        for index, row in enumerate(csv_reader):
            if index == 0:
                continue  # Skip header
            languages[row.get("lid_language")] = {
                "wikicode": row.get("wikicode"),
                "languagename": row.get("language_name"),
            }
        return languages

    def create_iso_lookup(self) -> Dict[str, str]:
        csv_path = os.path.join(current_dir, "languages-3-2.csv")
        csv_reader = csv.DictReader(open(csv_path))
        languages: Dict[str, str] = {}
        for index, row in enumerate(csv_reader):
            if index == 0:
                continue  # Skip header
            languages[row.get("alpha2")] = {
                "alpha3-b": row.get("alpha3-b"),
            }
        return languages

    def load(self):
        self.model = fasttext.load_model(model_path)
        self.ready = True

    def predict(self, text: str) -> Dict:
        if text is None:
            logging.error("Missing text in input data.")
            raise Exception("The parameter text is required.")

        label, score = self.model.predict(text.split("\n")[0])
        language = label[0].replace("__label__", "")

        wikicode = self.languages.get(language).get("wikicode")
        return {
            "language": language,
            "wikicode": self.languages.get(language).get("wikicode"),
            "languagename": self.languages.get(language).get("languagename"),
            "alpha3": self.alpha2_3_languages.get(wikicode).get("alpha3-b"),
            "score": score[0],
        }
