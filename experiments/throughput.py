import time
from pathlib import Path

from ThroughputExperiment import ThroughputExperiment
from experiments.ExperimentData import ThroughputExperimentData
from experiments.parsers import SynchronousSequenceTraceParser
from experiments.throughput.executors import FunctionWorkflowExecutor

all_experiment_data = []

sequence_experiment_data = ThroughputExperimentData(
        name='sequence',
        parser=SynchronousSequenceTraceParser.SynchronousSequenceTraceParser(),
        workflow_executor=FunctionWorkflowExecutor.FunctionWorkflowExecutor
    )

all_experiment_data.append(sequence_experiment_data)

for experiment_data in all_experiment_data:
    experiment = ThroughputExperiment(experiment_data=experiment_data)
    experiment.start()
    results_df = experiment.get_results()
    print(results_df)
    name = experiment.get_experiment_name()
    results_df['composition'] = name

    Path(f'results/{name}').mkdir(parents=True, exist_ok=True)
    results_df.to_csv(f'results/{name}/{int(time.time())}.csv', index=False)