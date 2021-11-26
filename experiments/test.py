
from datetime import datetime, timedelta, timezone
from XRayWrapper import XRayWrapper

client = XRayWrapper()

trace_ids = [
    '1-61a0cc24-6144a6be3fddd00808710e2d'
]
summaries = client.xray_client.batch_get_traces(TraceIds=trace_ids)

print(summaries)
# print(datetime.utcnow())