from collections import defaultdict


class EntityForm:
    def __init__(self):
        self._score = 0.
        self.forms = defaultdict(float)

    def add_form(self, score, normal_form):
        self._score += score
        self.forms[normal_form] = max(score, self.forms[normal_form])

    def normal_form(self):
        return max(self.forms.items(), key=lambda x: x[1])[0]

    @property
    def score(self):
        return self._score


class NamedObject:
    def __init__(self):
        self._entities = defaultdict(EntityForm)

    def __bool__(self):
        return bool(self._entities)

    def add(self, object_type, score, normal_form):
        self._entities[object_type].add_form(score, normal_form)

    def identify(self, score_threshold):
        # In the _entities map we have all objects grouped by category
        # (note both Name and Surname are actually general name category)
        # So if any entity can be Name or Surname with some score
        # assume that score of that entity be a _general name_ is sum of scores

        # Now we should arrange final category for every entity
        # based on categories scores

        # And we should drop objects that scores are not enough
        # (consider them trash)

        selected_category = None
        selected_score = -1
        selected_form = None
        for category, form in self._entities.items():
            if form.score > score_threshold and form.score > selected_score:
                selected_category, selected_score, selected_form = category, form.score, form.normal_form()

        if selected_category:
            yield selected_category, selected_form
