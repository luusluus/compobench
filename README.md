# Serverless Function Compositions Programmability Experiment
Each composition directory contains the dependencies it needs. This is done to evaluate programmability metrics such as LOC, CC etc.

Go to master branch to build, deploy and test compositions.
## Requirements
- Python3
- Radon

## Initial Setup
Install python package
```
python3 -m venv venv && source ./venv/bin/activate && pip install -e .
```

## Measure Cyclomatic Complexity (CC)

```
radon 
```