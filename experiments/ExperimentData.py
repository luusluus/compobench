from executors.WorkflowExecutor import WorkflowExecutor
from parsers.TraceParser import TraceParser

class ThroughputExperimentData:
    def __init__(
        self,
        name: str,
        workflow_executor: WorkflowExecutor,
    ):
        self.name = name
        # self.parser = parser
        self.workflow_executor = workflow_executor