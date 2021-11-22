from abc import ABC, abstractmethod
import json
import pandas as pd
from datetime import datetime

class TraceParser(ABC):
    def __init__(self):
        self._all_results = []
        self._aggregate_results = []
        self._workflow_ids = None

    def get_all_results(self):
        return self._all_results

    def get_aggregate_results_df(self):
        return pd.DataFrame(self._aggregate_results)

    def parse(self, traces):
        grouped_traces = self.group_traces_by_workflow_id(traces=traces)

        self.calculate_overheads(traces=grouped_traces)

    def convert_unix_timestamp_to_datetime_utc(self, unix_timestamp):
        return datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
    @abstractmethod
    def parse_trace(self, trace):
        pass

    def group_traces_by_workflow_id(self, traces):
        grouped_traces = {}
        for trace in traces:
            for segment in trace['Segments']:
                document = json.loads(segment['Document'])
                if document['origin'] == "AWS::Lambda::Function":
                    for subsegment in document['subsegments']:
                        if 'subsegments' in subsegment:
                            for subsubsegment in subsegment['subsegments']:
                                if subsubsegment['name'] == 'Identification':
                                    workflow_id = subsubsegment['annotations']['workflow_id']
                                    if workflow_id not in grouped_traces:
                                        grouped_traces[workflow_id] = []
                                    
                                    document['trace_id'] = trace['Id']
                                    grouped_traces[workflow_id].append(document)

        print(json.dumps(grouped_traces, sort_keys=True, indent=4, default=str))
        return grouped_traces


    def get_response_time(self, trace):
        # ResponseTime / makespan
        # The length of time in seconds between the start and end times of the root segment. 
        # If the service performs work asynchronously, the response time measures the time before the response is sent to the user, 
        # while the duration measures the amount of time before the last traced activity completes.
        first_segment = min(trace, key=lambda x: x['start_time'])

        start_time_root_segment = first_segment['start_time']
        end_time_root_segment = first_segment['end_time']
        return end_time_root_segment - start_time_root_segment

    def get_duration(self, trace):
        # Duration
        # The length of time in seconds between the start time of the root segment and the end time of the last segment that completed
        first_segment = min(trace, key=lambda x: x['start_time'])

        start_time_root_segment = first_segment['start_time']
        last_segment = max(trace, key=lambda x: x['end_time'])
        end_time = last_segment['end_time']

        # print(end_time-start_time_root_segment)
        # print(end_time_root_segment-start_time_root_segment)
        return end_time-start_time_root_segment

    def calculate_overheads(self, traces):
        for workflow_id, trace in traces.items():
            response_time = self.get_response_time(trace=trace) # makespan
            duration = self.get_duration(trace=trace)

            all_function_data = self.parse_trace(trace=trace)
            overhead = response_time
            for key, value in all_function_data.items():
                overhead -= value['execution_time']

            all_function_data['response_time'] = response_time
            all_function_data['duration'] = duration
            all_function_data['overhead'] = overhead
            all_function_data['workflow_id'] = workflow_id

            aggregate_function_data = {}
            aggregate_function_data['response_time'] = response_time
            aggregate_function_data['duration'] = duration
            aggregate_function_data['overhead'] = overhead
            aggregate_function_data['workflow_id'] = workflow_id

            self._all_results.append(all_function_data)
            self._aggregate_results.append(aggregate_function_data)

