from datetime import datetime, timedelta
from XRayWrapper import XRayWrapper

now = datetime.utcnow()
start = now - timedelta(minutes=12)
end = now + timedelta(minutes=12)
wrapper = XRayWrapper()

print(start)
print(end)
wrapper.get_trace_summaries(start, end)