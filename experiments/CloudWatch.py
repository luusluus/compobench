import boto3

class CloudWatch:
    def __init__(self):
        self.client = boto3.client('cloudwatch')

    def get_metric_statistics(self, metric_name, start, end):
        return self.client.get_metric_statistics(
            Namespace='AWS/Lambda',
            MetricName=metric_name,
            StartTime=start,
            EndTime=end,
            Statistics=['Sum'],
            Period=60, # seconds
    )

    def get_statistics(self, metric_name, start, end):
        statistics = self.get_metric_statistics(metric_name=metric_name, start=start, end=end)
        datapoints = statistics['Datapoints']
        if len(datapoints) == 1:
            return datapoints[0]['Sum']
        elif len(datapoints) == 2:
            return datapoints[1]['Sum']
        else:
            return 0
