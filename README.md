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


