from executors.WorkflowExecutor import WorkflowExecutor
from parsers.TraceParser import TraceParser
class ExperimentData:
    def __init__(
        self,
        name: str,
        amount_of_workflows: int,
        workflow_executor: WorkflowExecutor,
        parser: TraceParser
    ):
        self.name = name
        self.amount_of_workflows = amount_of_workflows
        self.workflow_executor = workflow_executor
        self.parser = parser