import json

from .TraceParser import TraceParser
# makespan 

# T_makespan =  t_end - t_start

# overhead

# T_overhead = T_makespan - sum(T_end_invocation_i - T_start_invocation_i) 

# get segment of function a, as workflow starts and ends here.

class SynchronousSequenceTraceParser(TraceParser):
    # TODO: get more fine-grained overhead. Startup overhead, and communication overhead
    def parse_traces(self, traces):
        all_function_data = {}
        for trace in traces:
            for segment in trace['Segments']:
                document = json.loads(segment['Document'])
                if document['origin'] == "AWS::Lambda::Function":
                    all_function_data[document['name']] = {}
                    for subsegment in document['subsegments']:
                        # get invocation start time
                        if subsegment['name'] == 'Invocation':
                            start_time = subsegment['start_time']
                            all_function_data[document['name']]['start_time'] = start_time
                            all_function_data[document['name']]['start_time_utc'] = self.convert_unix_timestamp_to_datetime_utc(start_time)
                            # get time invoking new lambda
                            if 'subsegments' in subsegment:
                                subsubsegment = subsegment['subsegments'][0]
                                end_time = subsubsegment['start_time']
                            else:
                                end_time = subsegment['end_time']
                            all_function_data[document['name']]['end_time'] = end_time
                            all_function_data[document['name']]['end_time_utc'] = self.convert_unix_timestamp_to_datetime_utc(end_time)

                            all_function_data[document['name']]['execution_time'] = end_time - start_time
                            all_function_data[document['name']]['trace_id'] = document['trace_id']

                        # The Overhead subsegment represents the phase that occurs between the time when the runtime sends 
                        # the response and the signal for the next invoke. 
                        # During this time, the runtime finishes all tasks related to an invoke and prepares to freeze the sandbox.
                        # if subsegment['name'] == 'Overhead':
                        #     function_runtime['extra_overhead_start_time'] = subsegment['start_time']
                        #     function_runtime['extra_overhead_end_time'] = subsegment['end_time']

        return all_function_data

