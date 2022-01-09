

import pandas as pd
from datetime import datetime, timedelta, timezone

from CloudWatch import CloudWatch
# start = datetime(year=2022, month=1, day=9, hour=16, minute=30, second=1, tzinfo=timezone.utc)
# end = datetime(year=2022, month=1, day=9, hour=16, minute=50, second=14, tzinfo=timezone.utc)


cloudwatch = CloudWatch()

# result = cloudwatch.get_metric_data(metric_name='Invocations', start=start, end=end)
# print(result)
statistic = 'Sum'
error_count = cloudwatch.get_statistics(metric_name='Errors', statistic=statistic, start=start, end=end)
invocation_count = cloudwatch.get_statistics(metric_name='Invocations', statistic=statistic, start=start, end=end)
throttle_count = cloudwatch.get_statistics(metric_name='Throttles', statistic=statistic, start=start, end=end)

if invocation_count > 0:
    error_rate = error_count / invocation_count
else:
    error_rate = 0

print(invocation_count)
print(error_rate)
print(throttle_count)


