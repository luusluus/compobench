import time
import json
import uuid
from OverheadExperiment import OverheadExperiment
from ExperimentData import ExperimentData, InvocationType
from parsers import CoordinatorTraceParser, SynchronousSequenceTraceParser, CompiledTraceParser, AsyncCoordinatorTraceParser

all_experiment_data = []

# synchronous function sequence
# sync_func_seq_experiment_data = ExperimentData(
#     name = 'Synchronous Function Sequence Experiment',
#     first_function_name = 'SequenceFunctionA', 
#     payload = {
#         'result': ''
#     }, 
#     amount_of_workflows = 1, 
#     invocation_type = InvocationType.Synchronous,
#     parser=SynchronousSequenceTraceParser.SynchronousSequenceTraceParser()
# )
# all_experiment_data.append(sync_func_seq_experiment_data)

# synchronous coordinator
# coordinator_experiment_data = ExperimentData(
#     name = 'Synchronous Coordinator Experiment',
#     first_function_name = 'CoordinatorFunctionCoordinator', 
#     payload = {
#         'workflow': ['CoordinatorFunctionA', 'CoordinatorFunctionB', 'CoordinatorFunctionC'],
#         'input': ''
#     },
#     amount_of_workflows = 1, 
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

# async coordinator
# async_coordinator_experiment_data = ExperimentData(
#     name = 'Asynchronous Coordinator Composition Experiment',
#     first_function_name = 'AsyncCoordinatorFunctionCoordinator', 
#     payload = {
#         'workflow': ['AsyncCoordinatorFunctionA', 'AsyncCoordinatorFunctionB', 'AsyncCoordinatorFunctionC'],
#         'input': '',
#     },
#     amount_of_workflows = 1, 
#     invocation_type = InvocationType.Asynchronous,
#     parser=AsyncCoordinatorTraceParser.AsyncCoordinatorTraceParser()
# )

# all_experiment_data.append(async_coordinator_experiment_data)

for experiment_data in all_experiment_data:
    experiment = OverheadExperiment(experiment_data=experiment_data)
    experiment.start()
    print(experiment.get_results(is_dataframe=True))
    results = experiment.get_results(is_dataframe=False)

    print(json.dumps(results, sort_keys=True, indent=4, default=str))
    # wait before next experiment
    # time.sleep(60)