# Serverless Function Compositions Cost Experiment

## Initial Setup
Install R Studio from (here)[https://www.rstudio.com/products/rstudio/download/].
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
