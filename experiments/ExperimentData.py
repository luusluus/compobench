from executors.WorkflowExecutor import WorkflowExecutor

class ThroughputExperimentData:
    def __init__(
        self,
        name: str,
        workflow_executor: WorkflowExecutor,
    ):
        self.name = name
        self.workflow_executor = workflow_executor