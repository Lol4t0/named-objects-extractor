from collections import defaultdict, namedtuple
import re
import pymorphy2

from .named_object import NamedObject


class ObjectExtractor:
    def __init__(self, score_threshold=0.51):
        self._score_threshold = score_threshold
        self._analyzer = pymorphy2.MorphAnalyzer()
        self._token_regex = re.compile(r"(?u)[a-zA-Zа-яА-Я][\w-]{2,}")
        self._space_regex = re.compile(r"(?u)^[\s\xa0\t]+$")

        self._tags_in_question = {
            'Name': 'people',
            'Surn': 'people',
            'Patr': 'people',

            'Geox': 'place',

            'Orgn': 'organization',
            'Trad': 'organization',
        }

    ObjectInfo = namedtuple('ObjectInfo', 'original normal_form pos')
    ObjectGroupInfo = namedtuple('ObjectGroupInfo', 'normal_form originals')

    def extract(self, text):
        self._text = text  # Who use threads anyway?

        objects = defaultdict(list)
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
                for category, normal_form in obj.identify(self._score_threshold):
                    objects[category].append(self.ObjectInfo(word, {normal_form}, pos))

        for category, entities in objects.items():
            objects[category] = list(self._make_dict(self._join_same_entities(self._join_adjacent_entities(entities))))

        return objects

    def _join_adjacent_entities(self, entities):
        joined = []
        entities.reverse()
        left = entities.pop()
        while entities:
            right = entities.pop()
            if self._no_punctuation(left.pos[1], right.pos[0]):
                start = left.pos[0]
                end = right.pos[1]
                left = self.ObjectInfo(self._text[start:end], left.normal_form.union(right.normal_form), (start, end))
            else:
                joined.append(left)
                left = right
        joined.append(left)
        return joined

    def _no_punctuation(self, start, end):
        text = self._text[start:end]
        return bool(self._space_regex.match(text)) and '\n' not in text

    def _join_same_entities(self, entities):
        # Select objects with the most of normal forms first
        entities.sort(key=lambda x: len(x.normal_form))

        for i, e in enumerate(entities):
            entities[i] = self.ObjectGroupInfo(e.normal_form, [(e.original, e.pos)])

        r = []

        for src in entities:
            added = False
            for i, dst in enumerate(r):
                if src.normal_form == dst.normal_form \
                        or src.normal_form in dst.normal_form \
                        or dst.normal_form in src.normal_form:
                    originals = src.originals + dst.originals
                    r[i] = self.ObjectGroupInfo(src.normal_form.union(dst.normal_form), originals)
                    added = True
                    break
            if not added:
                r.append(src)
        return r

    def _make_dict(self, entities):
        for entity in entities:
            yield {
                'name': tuple(entity.normal_form),
                'original': self._join_originals(entity.originals),
                'count': len(entity.originals)
            }

    @staticmethod
    def _join_originals(originals):
        d = defaultdict(list)
        for name, pos in originals:
            d[name].append(pos)
        return d
