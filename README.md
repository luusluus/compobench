# Serverless Function Compositions Programmability Experiment
Each composition directory contains the dependencies it needs. This is done to evaluate programmability metrics such as LOC, CC etc.

Go to master branch to build, deploy and test compositions.
## Requirements
- Python3
- Radon
- cloc

## Initial Setup
Install python package (radon)
```
python3 -m venv venv && source ./venv/bin/activate && pip install -e .
```
Install cloc
```
sudo apt install cloc
```
## Measure Lines of Code (LOC)
Python files
```
radon raw . -s
```

YAML & JSON files
```
cloc template.yaml
```

## Measure Cyclomatic Complexity (CC)

```
radon cc . -sa
```