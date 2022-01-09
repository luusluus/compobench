import boto3

class CloudWatch:
    def __init__(self):
        self.client = boto3.client('cloudwatch')

    def get_metric_statistics(self, metric_name, statistic, start, end, period):
        return self.client.get_metric_statistics(
            Namespace='AWS/Lambda',
            MetricName=metric_name,
            StartTime=start,
            EndTime=end,
            Statistics=[statistic],
            Period=period, # seconds
    )


    def get_metric_data(self, metric_name, start, end, period):
        self.client.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'invocation_count',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/Lambda',
                            'MetricName': metric_name,
                            'Dimensions': [
                                {
                                    'Name': 'string',
                                    'Value': 'string'
                                },
                            ]
                        },
                        'Period': 60,
                        'Stat': 'Sum',
                    },
                },
            ],
            StartTime=start,
            EndTime=end,

        )

    def get_statistics(self, metric_name, statistic, start, end, period):
        statistics = self.get_metric_statistics(metric_name=metric_name, statistic=statistic, start=start, end=end, period=period)
        datapoints = statistics['Datapoints']
        if len(datapoints) > 0:
            datapoint_sums = [datapoint['Sum'] for datapoint in datapoints if datapoint['Timestamp'] >= start]
            return sum(datapoint_sums)
        else:
            # TODO: Raise exception
            return 0
        
