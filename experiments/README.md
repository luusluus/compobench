# Experiments

## Initial Setup
Install venv
```
sudo apt-get update
sudo apt-get install python3.8-venv
```

Install python package
```
python3 -m venv venv && source ./venv/bin/activate && pip install -e .
```

## Throughput Performance
Increase File Descriptor Limit
https://muhammadtriwibowo.medium.com/set-permanently-ulimit-n-open-files-in-ubuntu-4d61064429a

Install hey
```
sudo apt-get update
sudo apt-get install hey
```

Run throughput experiment
```
cd experiments
python3 throughput.py
```