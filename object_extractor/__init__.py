from .extractor import ObjectExtractor


def extract_objects(text):
    object_extractor = ObjectExtractor()
    return object_extractor.extract(text)
