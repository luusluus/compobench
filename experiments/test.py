import json
from collections import OrderedDict
from operator import getitem


with open('data.json') as json_file:
    data = json.load(json_file)
    print(len(data['335fb01e-9eb1-4156-9c30-92f92e9adab3']))
    results = {k: {} for k, v in data.items()}
    for workflow, traces in data.items():
        result = []
        done = set()
        for trace in traces:
            trace_id = trace['Id']
            if trace_id not in done:
                done.add(trace_id)
                result.append(trace)
        
        results[workflow] = result

    print(len(results['335fb01e-9eb1-4156-9c30-92f92e9adab3']))
