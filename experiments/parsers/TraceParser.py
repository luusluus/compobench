from abc import ABC, abstractmethod
import json
import pandas as pd
from datetime import datetime


class NotEnoughTracesException(Exception):
    pass
class TraceParser(ABC):
    def __init__(self):
        self._all_results = []
        self._aggregate_results = []

    def reset(self):
        self._all_results = []
        self._aggregate_results = []

    def get_all_results(self):
        return self._all_results

    def get_aggregate_results_df(self, cold_start):
        df = pd.DataFrame(self._aggregate_results)
        if cold_start:
            df['is_cold'] = 'cold'
        else:
            df['is_cold'] = 'warm'
        return df

    def parse(self, traces, is_sync: bool):
        workflows = self.group_traces_by_workflow_id(traces=traces)
        self.calculate_overheads(workflows=workflows, is_sync=is_sync)

    def convert_unix_timestamp_to_datetime_utc(self, unix_timestamp):
        return datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
    @abstractmethod
    def parse_traces(self, traces):
        pass

    def remove_duplicate_traces(self, grouped_traces):
        results = {k: {} for k, v in grouped_traces.items()}
        for workflow, traces in grouped_traces.items():
            result = []
            done = set()
            for trace in traces:
                trace_id = trace['Id']
                if trace_id not in done:
                    done.add(trace_id)
                    result.append(trace)
            
            results[workflow] = result
        return results

    def order_grouped_traces_by_start_time(self, grouped_traces):
        for workflow_instance_id, traces in grouped_traces.items():
            for trace in traces:
                segments = []
                for segment in trace['Segments']:
                    document = json.loads(segment['Document'])
                
                    segments.append({
                        'Id': segment['Id'],
                        'Document': document
                    })

                segments = sorted(segments, key=lambda x: x['Document']['start_time'])
                trace['Segments'] = segments
        return grouped_traces

    def group_traces_by_workflow_id(self, traces):
        # TODO: add root node to grouped_traces to get full duration
        grouped_traces = {}
        for trace in traces:
            for segment in trace['Segments']:
                document = json.loads(segment['Document'])
                if "origin" in document:
                    if document["origin"] == "AWS::Lambda::Function":
                        for subsegment in document['subsegments']:
                            if 'subsegments' in subsegment:
                                for subsubsegment in subsegment['subsegments']:
                                    if subsubsegment['name'] == 'Identification':
                                        workflow_instance_id = subsubsegment['annotations']['workflow_instance_id']
                                        if workflow_instance_id not in grouped_traces:
                                            grouped_traces[workflow_instance_id] = []
                                        
                                        document['trace_id'] = trace['Id']
                                        grouped_traces[workflow_instance_id].append(trace)

                elif document['name'] == 'Client':
                    workflow_instance_id = document['annotations']['workflow_instance_id']
                    if workflow_instance_id not in grouped_traces:
                        grouped_traces[workflow_instance_id] = []
                    
                    grouped_traces[workflow_instance_id].append(trace)


        # remove duplicates in list
        grouped_traces = self.remove_duplicate_traces(grouped_traces=grouped_traces)
        # print(json.dumps(grouped_traces, sort_keys=True, indent=4, default=str))
        # order traces by start time
        grouped_traces = self.order_grouped_traces_by_start_time(grouped_traces)

        with open('data.json', 'w') as fp:
            json.dump(grouped_traces, fp,  indent=4, default=str)
        return grouped_traces

    def calculate_overheads(self, workflows, is_sync: bool):
        for workflow_instance_id, traces in workflows.items():
            # if len(traces) < 3:
            #     print(f'not enough traces in {workflow_instance_id}')
            #     continue
            parsed_traces = self.parse_traces(traces=traces)

            with open('result.json', 'w') as fp:
                json.dump(parsed_traces, fp,  indent=4, default=str)

            # FIXME: Check if function start is sync or async
            if is_sync:
                makespan = parsed_traces['response_time'] # makespan

            else:
                makespan = parsed_traces['duration']
            
            overhead = makespan
            for function_data in parsed_traces['function_data']:
                overhead -= function_data['execution_time']

            aggregate_data = {
                'makespan': makespan,
                'overhead': overhead,
                'workflow_instance_id': workflow_instance_id,
            }
            # all_function_data['makespan'] = makespan
            # all_function_data['overhead'] = overhead
            # all_function_data['workflow_instance_id'] = workflow_instance_id

            # self._all_results.append(all_function_data)
            self._aggregate_results.append(aggregate_data)

