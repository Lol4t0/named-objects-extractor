from collections import defaultdict
import re
import pymorphy2

from .named_object import NamedObject


class ObjectExtractor:
    def __init__(self):
        self._analyzer = pymorphy2.MorphAnalyzer()
        self._token_regex = re.compile(r"(?u)[a-zA-Zа-яА-Я][\w-]{2,}")

        self._tags_in_question = {
            'Name': 'people',
            'Surn': 'people',
            'Patr': 'people',

            'Geox': 'place',

            'Orgn': 'organization',
            'Trad': 'organization',
        }

    def extract(self, text):
        words = self._token_regex.findall(text)
        objects = defaultdict(list)
        for word in words:
            obj = NamedObject()
            forms = self._analyzer.parse(word)
            for form in forms:
                tags = form.tag
                for tag_to_check, category in self._tags_in_question.items():
                    if tag_to_check in tags:
                        obj.add(category, form.score, form.normal_form)
            if obj:
                forms = obj.calc_entities()
                for category, form in forms.items():
                    objects[category].append(self._make_object_record(word, form))

        return objects

    @staticmethod
    def _make_object_record(word, form):
        return {
            'name': form.normal_form(),
            'original': word,
            'score': form.score()
        }
