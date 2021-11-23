import boto3
from botocore.exceptions import ClientError

class XRayClient:
    def __init__(self):
        self._client = boto3.client('xray')

    def _get_trace_summaries(self, start, end):
        return self._client.get_trace_summaries(
            StartTime=start,
            EndTime=end
    )

    def batch_get_traces(self, start, end):

        summaries = self._get_trace_summaries(start, end)

        trace_ids = [summary['Id'] for summary in summaries['TraceSummaries']]

        for summary in summaries['TraceSummaries']:
            print(f'{summary["ResponseTime"]} | {summary["Duration"]} | {summary["Id"]}')

        try:
            batch_size = 5
            all_traces = []
            for i in range(0, len(trace_ids), batch_size):

                traces = self._client.batch_get_traces(
                    TraceIds=trace_ids[i: i + batch_size]
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

