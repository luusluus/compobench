from experiments.overhead.executors.WorkflowExecutor import WorkflowExecutor
from experiments.parsers.TraceParser import TraceParser

class OverheadExperimentData:
    def __init__(
        self,
        name: str,
        amount_of_workflows: int,
        repetitions: int,
        workflow_executor: WorkflowExecutor,
        parser: TraceParser
    ):
        self.name = name
        self.amount_of_workflows = amount_of_workflows
        self.repetitions = repetitions
        self.parser = parser
        self.workflow_executor = workflow_executor

class ThroughputExperimentData:
    def __init__(
        self,
        name: str,
        workflow_executor: WorkflowExecutor,
        parser: TraceParser
    ):
        self.name = name
        self.parser = parser
        self.workflow_executor = workflow_executor