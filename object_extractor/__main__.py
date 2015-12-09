import json
import sys
from .__init__ import extract_objects


if __name__ == "__main__":
    if len(sys.argv) < 2:
        file = sys.stdin
    else:
        file = open(sys.argv[1])

    text = file.read()
    print(json.dumps(extract_objects(text)))
