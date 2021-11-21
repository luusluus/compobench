import json

from .TraceParser import TraceParser
# makespan 

# T_makespan =  t_end - t_start

# overhead

# T_overhead = T_makespan - sum(T_end_invocation_i - T_start_invocation_i) 

# get segment of function a, as workflow starts and ends here.

class CoordinatorTraceParser(TraceParser):
    # TODO: get more fine-grained overhead. Startup overhead, and communication overhead
    def get_coordinator_data(self, trace):
        all_function_data = {}
        for segment in trace['Segments']:
            document = json.loads(segment['Document'])
            if document['origin'] == "AWS::Lambda::Function" and document['name'] == 'CoordinatorFunctionCoordinator':
                # all_function_data[document['name']] = {}
                for subsegment in document['subsegments']:
                    # get invocation start time
                    if subsegment['name'] == 'Invocation':
                        response_time = None
                        is_start = True
                        for subsubsegment in sorted(subsegment['subsegments'], key=lambda d: d['start_time']):
                            if is_start:
                                start_time = subsegment['start_time']
                                is_start = False
                            else:
                                start_time = response_time
                            name = 'CoordinatorFunctionCoordinator_' + subsubsegment['aws']['function_name']
                            if name not in all_function_data:
                                all_function_data[name] = {}
                            all_function_data[name]['start_time'] = start_time
                            all_function_data[name]['start_time_utc'] = self.convert_unix_timestamp_to_datetime_utc(start_time)

                            end_time = subsubsegment['start_time']
                            all_function_data[name]['end_time'] = end_time
                            all_function_data[name]['end_time_utc'] = self.convert_unix_timestamp_to_datetime_utc(end_time)
                            all_function_data[name]['execution_time'] = end_time - start_time
                            response_time = subsubsegment['end_time']
                return all_function_data


    def get_functions_data(self, trace):
        all_function_data = {}
        for segment in trace['Segments']:
            document = json.loads(segment['Document'])
            if document['origin'] == "AWS::Lambda::Function" and not document['name'] == 'CoordinatorFunctionCoordinator':
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

                    # The Overhead subsegment represents the phase that occurs between the time when the runtime sends 
                    # the response and the signal for the next invoke. 
                    # During this time, the runtime finishes all tasks related to an invoke and prepares to freeze the sandbox.
                    # if subsegment['name'] == 'Overhead':
                    #     function_runtime['extra_overhead_start_time'] = subsegment['start_time']
                    #     function_runtime['extra_overhead_end_time'] = subsegment['end_time']

        return all_function_data

    def parse_trace(self, trace):
        functions_data = self.get_functions_data(trace=trace)
        coordinator_data = self.get_coordinator_data(trace=trace)
        return {**functions_data, **coordinator_data}