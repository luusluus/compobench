import json

import boto3
from botocore.exceptions import ClientError
import pandas as pd

class NoTracesFoundException(Exception):
    pass
class XRayWrapper:
    def __init__(self):
        self.xray_client = boto3.client('xray')

    def _get_trace_summaries(self, start, end):
        return self.xray_client.get_trace_summaries(
            StartTime=start,
            EndTime=end
    )

    def batch_get_traces(self, start, end, workflow_instance_ids):
        print(start)
        print(end)
        summaries = self._get_trace_summaries(start, end)
        summaries_selected = []
        print(f'fetched {len(summaries["TraceSummaries"])} traces')
        # print(json.dumps(summaries["TraceSummaries"], indent=4))
        for summary in summaries['TraceSummaries']:
            if summary['Annotations']:
                workflow_instance_id = summary["Annotations"]["workflow_instance_id"][0]["AnnotationValue"]["StringValue"]
                if workflow_instance_id in workflow_instance_ids:
                    summaries_selected.append({
                        'response_time': summary["ResponseTime"],
                        'duration': summary["Duration"],
                        'trace_id': summary["Id"],
                        'workflow_instance_id': workflow_instance_id
                    })
        print(f'filtered to {len(summaries_selected)} traces')
        df = pd.DataFrame(summaries_selected)
        if len(df.index) == 0:
            raise NoTracesFoundException

        df.set_index('trace_id', inplace=True)
        print(df)

        trace_ids = df.index.tolist()
        try:
            batch_size = 5
            all_traces = []
            for i in range(0, len(trace_ids), batch_size):
                batch_trace_ids = trace_ids[i: i + batch_size]
                traces = self.xray_client.batch_get_traces(
                    TraceIds=batch_trace_ids
                )
                all_traces.extend(traces['Traces'])

            return self._merge_summaries_with_traces(traces=all_traces, summaries=summaries['TraceSummaries'])
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidRequestException':
                raise
            

    def _merge_summaries_with_traces(self, traces, summaries):
        for trace in traces:
            trace_id = trace['Id']
            response_time = next(summary['ResponseTime'] for summary in summaries if summary["Id"] == trace_id)
            trace['ResponseTime'] = response_time
        return traces

