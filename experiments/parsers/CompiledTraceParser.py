import json

from .TraceParser import TraceParser
# makespan 

# T_makespan =  t_end - t_start

# overhead

# T_overhead = T_makespan - sum(T_end_invocation_i - T_start_invocation_i) 

# get segment of function a, as workflow starts and ends here.

class CompiledTraceParser(TraceParser):
    def parse_trace(self, trace):
        all_function_data = {}
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
                        end_time = subsegment['end_time']
                        all_function_data[document['name']]['end_time'] = end_time
                        all_function_data[document['name']]['end_time_utc'] = self.convert_unix_timestamp_to_datetime_utc(end_time)

                        all_function_data[document['name']]['execution_time'] = end_time - start_time
                        return all_function_data