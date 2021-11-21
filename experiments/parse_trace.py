from datetime import datetime, timedelta, timezone

from TraceParser import TraceParser
from XRayClient import XRayClient
from OverheadExperiment import OverheadExperiment

experiment = OverheadExperiment(amount_of_workflows=10)
start = datetime(2021, 11, 20, 13, 18, 0, tzinfo=timezone.utc)
# fire off functions, then fetch traces
end = datetime(2021, 11, 20, 13, 19, 5, tzinfo=timezone.utc)

xray_client = XRayClient()

traces = xray_client.batch_get_traces(
    start=start, 
    end=end
)

parser = TraceParser()
parser.parse(traces=traces)


print(parser.get_aggregate_results_df())


