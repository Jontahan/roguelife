import json

def parse_spec(fname):
    with open(fname) as f:
        data = json.load(f)
        for key in data:
            if data[key]['dtype'] == 'float':
                data[key]['dtype'] = float
            if data[key]['dtype'] == 'int':
                data[key]['dtype'] = int
            if data[key]['dtype'] == 'bool':
                data[key]['dtype'] = bool
        return data