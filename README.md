# Serverless Function Compositions Throughput Experiment

## Requirements
- Python3
- Golang
- AWS account
- Installed AWS CLI and configured it with `aws configure` (https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)

## Initial Setup
### Install python package
```
python3 -m venv venv && source ./venv/bin/activate && pip install -e .
```

### Install AWS SAM CLI
https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-linux.html#serverless-sam-cli-install-linux-sam-cli

### Install HTTP Load Generator `hey`
https://github.com/rakyll/hey

## Building and deploying a composition
Deploy all compositions to AWS Lambda and X-Ray support.

### Build & Deploy All Compositions
```bash
bash ./deploy_sam_templates.sh
```

### Delete All Compositions
```bash
bash ./delete_sam_templates.sh
```

## Conduct Throughput Experiment
In `throughput.py` you configure the experiment parameters and which composition approaches you want to measure for their throughput.

The `all_experiment_data` list contains the selected composition approaches you want to measure in this experiment.

### Experiment
Start Proxy web serve:
```bash
go run main.go
```

Start throughput experiment
Run `throughput.py`.

### Observe executions in CloudWatch
Check the CloudWatch or Lambda web interface to see executions, failures and time-outs of each composition execution.

### Results
Results are found in `results` directory.
