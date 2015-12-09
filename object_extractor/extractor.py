from collections import defaultdict
import re
import pymorphy2

from .named_object import NamedObject


class ObjectExtractor:
    def __init__(self, score_threshold=0.6):
        self._score_threshold = score_threshold
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

    class ObjectRecord:
        def __init__(self):
            self._originals = defaultdict(list)
            self._total_score = 0.
            self._normal_form = None

        def add(self, original, normal_form, score, position):
            self._originals[original].append(position)
            assert not self._normal_form or self._normal_form == normal_form
            self._normal_form = normal_form
            self._total_score += score

        def to_dict(self):
            return {
                'name': self._normal_form,
                'original': self._originals,
                'score': self._total_score
            }

    def extract(self, text):
        objects = defaultdict(lambda: defaultdict(ObjectExtractor.ObjectRecord))
        for match in self._token_regex.finditer(text):
            word = match.group(0)
            pos = match.span(0)
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
                    if form.score() > self._score_threshold:
                        objects[category][form.normal_form()].add(word, form.normal_form(), form.score(), pos)

        r = {}

        for k, v in objects.items():
            r[k] = list(map(ObjectExtractor.ObjectRecord.to_dict, v.values()))

        return r

    @staticmethod
    def _make_object_record(word, form, pos):
        return {
            'name': form.normal_form(),
            'original': word,
            'score': form.score(),
            'position': pos
        }
