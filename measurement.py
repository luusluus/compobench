import os
import json
import subprocess

import pandas as pd
from radon.raw import analyze
from radon.visitors import ComplexityVisitor, Class, Function
from radon.complexity import cc_visit

def get_loc_json_yaml_file(file_path: str):
    bash_command = f'cloc {file_path} --json'

    process = subprocess.Popen(bash_command.split(' '), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return json.loads(output)['SUM']['code']

def get_loc_python_file(source_code: str):
    result = analyze(source_code)
    return result.sloc

def get_cyclomatic_complexity_sum(source_code: str):
    result = cc_visit(code=source_code)
    cc_sum = 0
    [cc_sum := cc_sum + symbol.complexity for symbol in result]
    
    blocks_amount = len(result)
    return cc_sum, blocks_amount

def determine_file_type(file_name):
    return file_name.split('.')[-1]

time_deltas_hours = {
    'sync-function-sequence': 5,
    'blackboard-based': 9,
    'client-side-scheduling': 0.25,
    'compiled-sequence': 0.0833,
    'coordinator': 0.75,
    'storage-based': 3,
    'routing-slip': 1.5,
    'event-sourcing': 15.75,
    'async-function-sequence': 5.5,
    'workflow-engine': 2.75,
    'message-queue-based': 5.25,
    'async-coordinator': 4.25

}
metrics = {}
base_dir = './compositions/'
for directory in os.listdir(base_dir):
    if directory in ['aws_helpers', 'continuations-checkpointing', 'continuations-actors']:
        continue

    composition_dir = base_dir + directory
    metrics[directory] = {
        'loc_py': 0,
        'loc_yaml': 0,
        'loc_total': 0,
        'time_delta': time_deltas_hours[directory]
    }
    cc_total_sum = 0
    cc_blocks_total_amount = 0
    for file_name in os.listdir(composition_dir):
        file_type = determine_file_type(file_name=file_name)
        file_path = composition_dir + '/' + file_name
        if file_type == 'yaml' or file_type == 'json':
            loc = get_loc_json_yaml_file(file_path=file_path)
            metrics[directory]['loc_yaml'] += loc
            metrics[directory]['loc_total'] += loc
        
        if file_type == 'py':
            f = open(file_path, 'r')
            source_code = f.read()
            loc = get_loc_python_file(source_code=source_code)
            metrics[directory]['loc_py'] += loc
            metrics[directory]['loc_total'] += loc
            
            cc_sum, cc_blocks_amount = get_cyclomatic_complexity_sum(source_code=source_code)
            cc_total_sum = cc_total_sum + cc_sum
            cc_blocks_total_amount = cc_blocks_total_amount + cc_blocks_amount
    
    if cc_blocks_total_amount != 0:
        metrics[directory]['cc_avg'] = cc_total_sum / cc_blocks_total_amount
    else:
        metrics[directory]['cc_avg'] = 0



df = pd.DataFrame.from_dict(metrics, orient='index')
print(df)
df.index.name = 'composition'
df.to_csv('./out.csv')