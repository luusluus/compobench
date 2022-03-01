# Serverless Function Compositions with AWS Lambda

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

First, go into one of the composition directories. For example:

```
cd compositions/sync-function-sequence
```

### Build
```
sam build
```

### Validate Template
Before deploying, validate the SAM YAML template
```
sam validate
```

### Deployment
First time
```
sam deploy --guided
```

For subsequent deployments
```
sam deploy
```

## Testing a composition
First activate virtual environment

```
source ./venv/bin/activate
```

Go into one of the composition directories and call the client script. For example:
```
cd compositions/sync-function-sequence
python3 client.py
```