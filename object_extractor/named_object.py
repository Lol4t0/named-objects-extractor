from collections import defaultdict


class EntityForm:
    def __init__(self):
        self._score = 0.
        self.forms = defaultdict(float)

    def add_form(self, score, normal_form):
        self._score += score
        self.forms[normal_form] += score

    def normal_form(self):
        return max(self.forms.items(), key=lambda x: x[1])[0]

    def score(self):
        return self._score


class NamedObject:
    def __init__(self):
        self._entities = []

    def __bool__(self):
        return bool(self._entities)

    def add(self, object_type, score, normal_form):
        self._entities.append((object_type, score, normal_form))

    def calc_entities(self):
        forms = defaultdict(EntityForm)
        forms['object'] = self._make_global_entity()
        for object_type, score, normal_form in self._entities:
            forms[object_type].add_form(score, normal_form)

        return forms

    def _make_global_entity(self):
        global_form = EntityForm()
        for _, score, form in self._entities:
            global_form.add_form(score, form)
        return global_form



