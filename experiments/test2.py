import sys

payload = {'workflow_instance_id': 'b4c3c483-c1b7-42f1-b127-d5ea73cdda09', 'sleep': 2}

size_bytes = sys.getsizeof(payload)

def bytesto(bytes, to, bsize=1024):
    """convert bytes to megabytes, etc.
       sample code:
           print('mb= ' + str(bytesto(314575262000000, 'm')))
       sample output: 
           mb= 300002347.946
    """

    a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
    r = float(bytes)
    for i in range(a[to]):
        r = r / bsize

    return(r)

print(size_bytes)
print(f'{bytesto(size_bytes, to="g"):.10f}')


