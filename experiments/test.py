import json

with open('executors/config.json') as json_file:
    data = json.load(json_file)
    print(data['sequence'])