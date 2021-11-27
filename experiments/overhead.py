import time
import json
import uuid

from OverheadExperiment import OverheadExperiment
from ExperimentData import ExperimentData
from parsers import CoordinatorTraceParser, SynchronousSequenceTraceParser, EventSourcingTraceParser
from executors import FunctionWorkflowExecutor, MessageQueueBasedWorkflowExecutor, StorageBasedWorkflowExecutor, WorkflowEngineBasedWorkflowExecutor
from executors.FunctionWorkflowExecutor import LambdaInvocationType

all_experiment_data = []

# synchronous function sequence
# sync_func_seq_experiment_data = ExperimentData(
#     name='Synchronous Function Sequence Experiment',
#     amount_of_workflows=1,
#     workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor(
#         payload={
#             'result': ''
#         }, 
#         lambda_invocation_type=LambdaInvocationType.Synchronous,
#         first_function_name='SequenceFunctionA',
#     ),
#     parser=SynchronousSequenceTraceParser.SynchronousSequenceTraceParser()
# )
# all_experiment_data.append(sync_func_seq_experiment_data)

# synchronous coordinator
# coordinator_experiment_data=ExperimentData(
#     name='Synchronous Coordinator Experiment',
#     amount_of_workflows=10, 
#     workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor(
#         payload={
#             'workflow': ['CoordinatorFunctionA', 'CoordinatorFunctionB', 'CoordinatorFunctionC'],
#             'input': ''
#         }, 
#         lambda_invocation_type=LambdaInvocationType.Synchronous,
#         first_function_name='CoordinatorFunctionCoordinator', 
#     ),
#     parser=CoordinatorTraceParser.CoordinatorTraceParser(
#         coordinator_function_name='CoordinatorFunctionCoordinator'
#     )
# )
# all_experiment_data.append(coordinator_experiment_data)

# compiled
# compiled_experiment_data = ExperimentData(
#     name='Compiled Composition Experiment',
#     amount_of_workflows=10, 
#     workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor(
#         payload={},
#         first_function_name='CompiledFunction',
#         lambda_invocation_type=LambdaInvocationType.Synchronous,
#     ),
#     parser=SynchronousSequenceTraceParser.SynchronousSequenceTraceParser()
# )
# all_experiment_data.append(compiled_experiment_data)

# async sequence
# async_sequence_experiment_data=ExperimentData(
#     name='Asynchronous Function Sequence',
#     amount_of_workflows=10,
#     workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor(
#         payload={
#             'result': ''
#         },
#         lambda_invocation_type=LambdaInvocationType.Asynchronous,
#         first_function_name='AsyncSequenceFunctionA',
#     ),
#     parser=SynchronousSequenceTraceParser.SynchronousSequenceTraceParser()
# )
# all_experiment_data.append(async_sequence_experiment_data)

# routing slip
# routing_slip_experiment_data=ExperimentData(
#     name='Routing Slip',
#     amount_of_workflows=10,
#     workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor(
#         payload={
#             'composition': ['RoutingSlipFunctionB', 'RoutingSlipFunctionC'],
#             'result': ''
#         },
#         first_function_name='RoutingSlipFunctionA',
#         lambda_invocation_type=LambdaInvocationType.Asynchronous
#     ),
#     parser=SynchronousSequenceTraceParser.SynchronousSequenceTraceParser()
# )
# all_experiment_data.append(routing_slip_experiment_data)

# async coordinator
# async_coordinator_experiment_data = ExperimentData(
#     name='Asynchronous Coordinator Composition Experiment',
#     amount_of_workflows=10,
#     workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor(
#         payload={
#             'workflow': ['AsyncCoordinatorFunctionA', 'AsyncCoordinatorFunctionB', 'AsyncCoordinatorFunctionC'],
#             'input': '',
#         }, 
#         lambda_invocation_type=LambdaInvocationType.Asynchronous, 
#         first_function_name='AsyncCoordinatorFunctionCoordinator'
#     ),
#     parser=CoordinatorTraceParser.CoordinatorTraceParser(coordinator_function_name='AsyncCoordinatorFunctionCoordinator')
# )
# all_experiment_data.append(async_coordinator_experiment_data)

# blackboard based
# TODO: missing traces, require 4, only get 2 or 3 sometimes
# blackboard_based_experiment_data=ExperimentData(
#     name='Blackboard Based Composition',
#     amount_of_workflows=1,
#     workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor(
#         payload={},
#         lambda_invocation_type=LambdaInvocationType.Asynchronous, 
#         first_function_name='BlackboardFunctionController'
#     ),
#     parser=CoordinatorTraceParser.CoordinatorTraceParser(coordinator_function_name='BlackboardFunctionController')
# )
# all_experiment_data.append(blackboard_based_experiment_data)

# event sourcing
event_sourcing_based_experiment_data=ExperimentData(
    name='Event Sourcing Based Composition',
    amount_of_workflows=1,
    workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor(
        payload={
            'input': ''
        }, 
        lambda_invocation_type=LambdaInvocationType.Asynchronous, 
        first_function_name='EventSourcingOrchestrator'
    ),
    parser=EventSourcingTraceParser.EventSourcingTraceParser(coordinator_function_name='EventSourcingOrchestrator')
)
all_experiment_data.append(event_sourcing_based_experiment_data)

# message queue based
# message_queue_based_experiment_data=ExperimentData(
#     name='Message Queue Based Composition',
#     amount_of_workflows=10,
#     parser=SynchronousSequenceTraceParser.SynchronousSequenceTraceParser(),
#     workflow_executor=MessageQueueBasedWorkflowExecutor(
#         payload={'result': ''},
#         message_attributes={
#             'caller': {
#                 'DataType': 'String',
#                 'StringValue': 'Client',
#             },
#             'last_function': {
#                 'DataType': 'String',
#                 'StringValue': 'MessageQueueFunctionC'
#             }
#         },
#     ),
# )
# all_experiment_data.append(message_queue_based_experiment_data)

# storage_based_experiment_data=ExperimentData(
#     name='Storage Based Composition',
#     amount_of_workflows=10,
#     parser=SynchronousSequenceTraceParser.SynchronousSequenceTraceParser(),
#     workflow_executor=StorageBasedWorkflowExecutor(
#         payload={
#             'workflow': ['function_b', 'function_c'],
#             'result': ''
#         },
#         bucket_name='storage-based-store',
#         first_function='function_a'
#     ),
# )
# all_experiment_data.append(storage_based_experiment_data)

# workflow_engine_based_experiment=ExperimentData(
#     name='Workflow Engine Based Composition',
#     amount_of_workflows=10,
#     parser=SynchronousSequenceTraceParser.SynchronousSequenceTraceParser(),
#     workflow_executor=WorkflowEngineBasedWorkflowExecutor(
#         payload={
#             'result': ''
#         },
#         stack_name='workflow-engine'
#     ),
# )
# all_experiment_data.append(workflow_engine_based_experiment)


for experiment_data in all_experiment_data:
    experiment = OverheadExperiment(experiment_data=experiment_data)
    experiment.start()
    print(experiment.get_results(is_dataframe=True))
    results = experiment.get_results(is_dataframe=False)

    # print(json.dumps(results, sort_keys=True, indent=4, default=str))
    # wait before next experiment
    # time.sleep(60)