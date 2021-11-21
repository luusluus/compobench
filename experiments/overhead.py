import time
import json
from OverheadExperiment import OverheadExperiment
from ExperimentData import ExperimentData, InvocationType
from parsers import CoordinatorTraceParser, SynchronousSequenceTraceParser, CompiledTraceParser

all_experiment_data = []

# # synchronous function sequence
# sync_func_seq_experiment_data = ExperimentData(
#     name = 'Synchronous Function Sequence Experiment',
#     first_function_name = 'SequenceFunctionA', 
#     payload = {
#         'result': ''
#     }, 
#     amount_of_workflows = 10, 
#     invocation_type = InvocationType.Synchronous
# )
# all_experiment_data.append(sync_func_seq_experiment_data)

# # synchronous coordinator
# coordinator_experiment_data = ExperimentData(
#     name = 'Synchronous Coordinator Experiment',
#     first_function_name = 'CoordinatorFunctionCoordinator', 
#     payload = {
#         'workflow': ['CoordinatorFunctionA', 'CoordinatorFunctionB', 'CoordinatorFunctionC'],
#         'input': ''
#     },
#     amount_of_workflows = 10, 
#     invocation_type = InvocationType.Synchronous,
#     parser=CoordinatorTraceParser.CoordinatorTraceParser()
# )
# all_experiment_data.append(coordinator_experiment_data)

# compiled
compiled_experiment_data = ExperimentData(
    name = 'Compiled Composition Experiment',
    first_function_name = 'CompiledFunction', 
    payload = {},
    amount_of_workflows = 10, 
    invocation_type = InvocationType.Synchronous,
    parser=CompiledTraceParser.CompiledTraceParser()
)

all_experiment_data.append(compiled_experiment_data)


for experiment_data in all_experiment_data:
    experiment = OverheadExperiment(experiment_data=experiment_data)
    experiment.start()
    print(experiment.get_results(is_dataframe=True))
    results = experiment.get_results(is_dataframe=False)

    print(json.dumps(results, sort_keys=True, indent=4, default=str))
    # wait before next experiment
    # time.sleep(60)