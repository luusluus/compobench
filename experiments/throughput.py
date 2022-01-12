import time
from pathlib import Path

from ThroughputExperiment import ThroughputExperiment
from ExperimentData import ThroughputExperimentData
from executors import FunctionWorkflowExecutor

all_experiment_data = []

sequence_experiment_data = ThroughputExperimentData(
    name='sequence',
    workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor
)

coordinator_experiment_data = ThroughputExperimentData(
    name='coordinator',
    workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor,
)

compiled_experiment_data = ThroughputExperimentData(
    name='compiled',
    workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor,
)

async_sequence_experiment_data = ThroughputExperimentData(
    name='async_sequence',
    workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor,
)

routing_slip_experiment_data = ThroughputExperimentData(
    name='routing_slip',
    workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor,
)

async_coordinator_experiment_data = ThroughputExperimentData(
    name='async_coordinator',
    workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor,
)

event_sourcing_experiment_data = ThroughputExperimentData(
    name='event_sourcing',
    workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor,
)

blackboard_experiment_data = ThroughputExperimentData(
    name='blackboard',
    workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor,
)

message_queue_experiment_data = ThroughputExperimentData(
    name='message_queue',
    workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor,
)

storage_based_experiment_data = ThroughputExperimentData(
    name='storage',
    workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor,
)

workflow_engine_experiment_data = ThroughputExperimentData(
    name='workflow_engine',
    workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor,
)

# all_experiment_data.append(sequence_experiment_data)
# all_experiment_data.append(coordinator_experiment_data)
# all_experiment_data.append(compiled_experiment_data)
# all_experiment_data.append(async_sequence_experiment_data)
# all_experiment_data.append(routing_slip_experiment_data)
all_experiment_data.append(async_coordinator_experiment_data)
# all_experiment_data.append(event_sourcing_experiment_data)
# all_experiment_data.append(blackboard_experiment_data)
# all_experiment_data.append(message_queue_experiment_data)
# all_experiment_data.append(storage_based_experiment_data)
# all_experiment_data.append(workflow_engine_experiment_data)

for experiment_data in all_experiment_data:
    experiment = ThroughputExperiment(experiment_data=experiment_data)
    experiment.start()
    hey_results_df = experiment.get_hey_results()
    aws_results_df = experiment.get_aws_results()

    hey_results_df.rename(columns={
            'response-time': 'response_time', 
            'DNS+dialup': 'dns_dialup',
            'Request-write': 'request_write',
            'Response-delay': 'response_delay',
            'Response-read': 'response_read',
            'status-code': 'status_code',
        },
        inplace=True)

    Path(f'results/{experiment_data.name}').mkdir(parents=True, exist_ok=True)
    hey_results_df.to_csv(f'results/{experiment_data.name}/hey_{int(time.time())}.csv', index=False)
    aws_results_df.to_csv(f'results/{experiment_data.name}/aws_{int(time.time())}.csv', index=False)