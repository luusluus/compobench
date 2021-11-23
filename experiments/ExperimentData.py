
class InvocationType:
    Synchronous = 'RequestResponse'
    Asynchronous = 'Event'

class ExperimentData:
    def __init__(
        self,
        name: str,
        first_function_name: str,
        payload: dict,
        amount_of_workflows: int,
        invocation_type: InvocationType,
        parser
    ):
        self.name = name
        self.first_function_name = first_function_name
        self.payload = payload
        self.amount_of_workflows = amount_of_workflows
        self.invocation_type = invocation_type
        self.parser = parser