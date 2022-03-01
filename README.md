# Serverless Function Compositions Overhead Experiment

## Requirements
- Python3
- AWS account
- Installed AWS CLI and configured it with `aws configure` (https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)

## Initial Setup
Install python package
```
python3 -m venv venv && source ./venv/bin/activate && pip install -e .
```

Install AWS SAM CLI

https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-linux.html#serverless-sam-cli-install-linux-sam-cli

## Building and deploying a composition
Deploy all compositions to AWS Lambda and X-Ray support.

### Build & Deploy All Compositions
```bash
bash ./deploy_sam_templates
```

## Conduct Overhead Experiment
In `overhead.py` you configure the experiment parameters and which composition approaches you want to measure for their overhead.

The variable `ROUNDS` indicates how many times an approach is repeated in one experiment.
The variable `AMOUNT_WORKFLOWS_PER_ROUND` indicates how many workflows (i.e., composition executions) are invoked in one round.

The `all_experiment_data` list contains the selected composition approaches you want to measure in this experiment.

### Start experiment
Run `overhead.py`.

### Observe executions in X-Ray
Check the AWS X-Ray web interface to see traces of each composition execution.

### Results
Results are found in `results` directory.
