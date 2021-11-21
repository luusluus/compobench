from abc import ABC, abstractmethod
import json
import pandas as pd
from datetime import datetime

class TraceParser(ABC):
    def __init__(self):
        self._all_results = []
        self._aggregate_results = []

    def get_all_results(self):
        return self._all_results

    def get_aggregate_results_df(self):
        return pd.DataFrame(self._aggregate_results)

    def parse(self, traces):
        for trace in traces:
            self.calculate_overhead(trace)

    def convert_unix_timestamp_to_datetime_utc(self, unix_timestamp):
        return datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
    @abstractmethod
    def parse_trace(self, trace):
        pass

    def get_response_time(self, trace):
        # ResponseTime / makespan
        # The length of time in seconds between the start and end times of the root segment. 
        # If the service performs work asynchronously, the response time measures the time before the response is sent to the user, 
        # while the duration measures the amount of time before the last traced activity completes.
        first_segment = min(trace['Segments'], key=lambda x: json.loads(x['Document'])['start_time'])
        first_segment = json.loads(first_segment['Document'])

        start_time_root_segment = first_segment['start_time']
        end_time_root_segment = first_segment['end_time']
        return end_time_root_segment - start_time_root_segment

    def get_duration(self, trace):
        # Duration
        # The length of time in seconds between the start time of the root segment and the end time of the last segment that completed
        first_segment = min(trace['Segments'], key=lambda x: json.loads(x['Document'])['start_time'])
        first_segment = json.loads(first_segment['Document'])

        start_time_root_segment = first_segment['start_time']
        last_segment = max(trace['Segments'], key=lambda x: json.loads(x['Document'])['end_time'])
        last_segment = json.loads(last_segment['Document'])
        end_time = last_segment['end_time']

        # print(end_time-start_time_root_segment)
        # print(end_time_root_segment-start_time_root_segment)
        return end_time-start_time_root_segment

    def calculate_overhead(self, trace):
        response_time = self.get_response_time(trace=trace) # makespan
        duration = self.get_duration(trace=trace)

        all_function_data = self.parse_trace(trace=trace)
        overhead = response_time
        for key, value in all_function_data.items():
            overhead -= value['execution_time']

        all_function_data['response_time'] = response_time
        all_function_data['duration'] = duration
        all_function_data['overhead'] = overhead
        all_function_data['trace_id'] = trace['Id']

        aggregate_function_data = {}
        aggregate_function_data['response_time'] = response_time
        aggregate_function_data['duration'] = duration
        aggregate_function_data['overhead'] = overhead
        aggregate_function_data['trace_id'] = trace['Id']

        self._all_results.append(all_function_data)
        self._aggregate_results.append(aggregate_function_data)

