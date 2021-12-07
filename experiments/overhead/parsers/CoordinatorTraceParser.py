from .TraceParser import TraceParser
# makespan 

# T_makespan =  t_end - t_start

# overhead

# T_overhead = T_makespan - sum(T_end_invocation_i - T_start_invocation_i) 

# get segment of function a, as workflow starts and ends here.

class CoordinatorTraceParser(TraceParser):
    def __init__(self, coordinator_function_name):
        super().__init__()
        self._coordinator_function_name = coordinator_function_name

    # TODO: get more fine-grained overhead. Startup overhead, and communication overhead
    def get_functions_data(self, traces):
        all_function_data = []
        for trace in traces:
            for segment in trace['Segments']:
                document = segment['Document']
                if document['origin'] == "AWS::Lambda::Function" and not document['name'] == self._coordinator_function_name:
                    function_data = {
                        'name': document['name']
                    }
                    for subsegment in document['subsegments']:
                        # get invocation start time
                        if subsegment['name'] == 'Invocation':
                            start_time = subsegment['start_time']
                            function_data['start_time'] = start_time
                            function_data['start_time_utc'] = self.convert_unix_timestamp_to_datetime_utc(start_time)
                        
                            end_time = subsegment['end_time']
                            function_data['end_time'] = end_time
                            function_data['end_time_utc'] = self.convert_unix_timestamp_to_datetime_utc(end_time)

                            function_data['execution_time'] = end_time - start_time
                            function_data['trace_id'] = document['trace_id']
                    all_function_data.append(function_data)
        return all_function_data

    def get_response_time(self, traces):
        # ResponseTime / makespan
        # The length of time in seconds between the start and end times of the root segment. 
        # If the service performs work asynchronously, the response time measures the time before the response is sent to the user, 
        # while the duration measures the amount of time before the last traced activity completes.
        return sum(trace['ResponseTime'] for trace in traces)

    def get_duration(self, traces):
        # Duration
        # The length of time in seconds between the start time of the root segment and 
        # the end time of the last segment that completed
        return sum(trace['Duration'] for trace in traces)

    def parse_traces(self, traces):
        function_data = self.get_functions_data(traces=traces)
        function_data = sorted(function_data, key=lambda d: d['start_time']) 

        return {
            'response_time': self.get_response_time(traces=traces),
            'duration': self.get_duration(traces=traces),
            'function_data': function_data
        }