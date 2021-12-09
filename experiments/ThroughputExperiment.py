class ThroughputExperiment:
    def __init__(self):
        pass

    def start(self, iterations):
        self.iterations = iterations
        self._xray_wrapper = XRayWrapper()