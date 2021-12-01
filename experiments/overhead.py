import time
import json
import uuid
from pathlib import Path

from OverheadExperiment import OverheadExperiment
from ExperimentData import ExperimentData
from parsers import CoordinatorTraceParser, SynchronousSequenceTraceParser, EventSourcingTraceParser, ClientsideSchedulingTraceParser
from executors import FunctionWorkflowExecutor, MessageQueueBasedWorkflowExecutor, StorageBasedWorkflowExecutor, WorkflowEngineBasedWorkflowExecutor, ClientsideWorkflowExecutor

all_experiment_data = []

# synchronous function sequence
sync_func_seq_experiment_data = ExperimentData(
    name='sequence',
    amount_of_workflows=100,
    repetitions=2,
    parser=SynchronousSequenceTraceParser.SynchronousSequenceTraceParser(),
    workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor
)

# synchronous coordinator
coordinator_experiment_data=ExperimentData(
    name='coordinator',
    amount_of_workflows=100,
    repetitions=2,
    parser=CoordinatorTraceParser.CoordinatorTraceParser(
        coordinator_function_name='CoordinatorFunctionCoordinator'
    ),
    workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor
)

# compiled
compiled_experiment_data = ExperimentData(
    name='compiled',
    amount_of_workflows=100,
    repetitions=2,
    parser=SynchronousSequenceTraceParser.SynchronousSequenceTraceParser(),
    workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor
)

# async sequence
async_sequence_experiment_data=ExperimentData(
    name='async_sequence',
    amount_of_workflows=100,
    repetitions=2,
    parser=SynchronousSequenceTraceParser.SynchronousSequenceTraceParser(),
    workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor
)

# routing slip
routing_slip_experiment_data=ExperimentData(
    name='routing_slip',
    amount_of_workflows=100,
    repetitions=2,
    parser=SynchronousSequenceTraceParser.SynchronousSequenceTraceParser(),
    workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor
)

# async coordinator
async_coordinator_experiment_data = ExperimentData(
    name='async_coordinator',
    amount_of_workflows=100,
    repetitions=2,
    parser=CoordinatorTraceParser.CoordinatorTraceParser(coordinator_function_name='AsyncCoordinatorFunctionCoordinator'),
    workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor
)

# blackboard based
# FIXME: missing traces, require 4, only get 2 or 3 sometimes
# blackboard_based_experiment_data=ExperimentData(
#     name='Blackboard Based Composition',
#     amount_of_workflows=100,
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
    name='event_sourcing',
    amount_of_workflows=100,
    repetitions=2,
    parser=EventSourcingTraceParser.EventSourcingTraceParser(coordinator_function_name='EventSourcingOrchestrator'),
    workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor
)

# message queue based
message_queue_based_experiment_data=ExperimentData(
    name='message_queue',
    amount_of_workflows=100,
    repetitions=2,
    parser=SynchronousSequenceTraceParser.SynchronousSequenceTraceParser(),
    workflow_executor=MessageQueueBasedWorkflowExecutor.MessageQueueBasedWorkflowExecutor
)

# storage based
storage_based_experiment_data=ExperimentData(
    name='storage',
    amount_of_workflows=100,
    repetitions=2,
    parser=SynchronousSequenceTraceParser.SynchronousSequenceTraceParser(),
    workflow_executor=StorageBasedWorkflowExecutor.StorageBasedWorkflowExecutor
)

# workflow engine based
workflow_engine_based_experiment=ExperimentData(
    name='workflow_engine',
    amount_of_workflows=100,
    repetitions=2,
    parser=SynchronousSequenceTraceParser.SynchronousSequenceTraceParser(),
    workflow_executor=WorkflowEngineBasedWorkflowExecutor.WorkflowEngineBasedWorkflowExecutor
)

# client side scheduling. Requires xray daemon locally or on ec2
# ./xray -o -n eu-central-1
client_side_based_experiment=ExperimentData(
    name='client_side',
    amount_of_workflows=10,
    repetitions=2,
    parser=ClientsideSchedulingTraceParser.ClientsideSchedulingParser(),
    workflow_executor=ClientsideWorkflowExecutor.ClientsideWorkflowExecutor
)


# comment out experiments
all_experiment_data.append(sync_func_seq_experiment_data)
all_experiment_data.append(coordinator_experiment_data)
all_experiment_data.append(compiled_experiment_data)
all_experiment_data.append(async_sequence_experiment_data)
all_experiment_data.append(routing_slip_experiment_data)
all_experiment_data.append(async_coordinator_experiment_data)
all_experiment_data.append(event_sourcing_based_experiment_data)
all_experiment_data.append(message_queue_based_experiment_data)
all_experiment_data.append(storage_based_experiment_data)
all_experiment_data.append(workflow_engine_based_experiment)
all_experiment_data.append(client_side_based_experiment)

for experiment_data in all_experiment_data:
    experiment = OverheadExperiment(experiment_data=experiment_data)
    experiment.start()
    results_df = experiment.get_results()
    print(results_df)
    name = experiment.get_experiment_name()
    results_df['composition'] = name
    Path(f'results/{name}').mkdir(parents=True, exist_ok=True)
    results_df.to_csv(f'results/{name}/{int(time.time())}.csv', index=False)
    
    # wait before next experiment