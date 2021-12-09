from abc import ABC, abstractmethod
import pathlib

import json
class WorkflowExecutor(ABC):
    def __init__(self, composition_name, workflow_instance_id):
        # TODO: load from config into dict
        self.config = self.read_from_config(composition_name=composition_name)
        self.workflow_instance_id = workflow_instance_id

    @abstractmethod
    def start(self):
        pass

    # @property
    # def config(self):
    #     return self.config

    # @config.setter
    # def payload(self, value):
    #     self.config = value

    def read_from_config(self, composition_name):
        with open(f'{pathlib.Path(__file__).parent.resolve()}/config.json') as json_file:
            config = json.load(json_file)
            return config[composition_name]