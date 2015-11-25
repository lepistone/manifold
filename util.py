from json import loads, dumps


def pretty_json(line):
    return dumps(loads(line), indent=4)
