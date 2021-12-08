# Experiments

## Initial Setup
Install python package
```
python3 -m venv venv && source ./venv/bin/activate && pip install -e .
```

## Overhead Performance

### AWS X-Ray Daemon
Install X-Ray Daemon
```
BUCKETURL=https://s3.us-east-2.amazonaws.com/aws-xray-assets.us-east-2
wget $BUCKETURL/xray-daemon/aws-xray-daemon-linux-3.0.0.zip
unzip aws-xray-daemon-linux-3.0.0.zip -d xray
```

Run X-Ray Daemon
```
cd xray
./xray -o -n eu-central-1
```

### Run Experiment
Adjust `overhead.py` for experiment selection, experiment round amount and workflow amount per round.

Run overhead experiment
```
cd experiments/overhead
python3 overhead.py
```

## Throughput Performance
Install hey
```
sudo apt-get update
sudo apt-get install hey
```

Run throughput experiment
```
cd experiments/throughput
python3 throughput.py
```