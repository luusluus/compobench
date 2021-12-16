# Experiments

## Initial Setup
Install python package
```
python3 -m venv venv && source ./venv/bin/activate && pip install -e .
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