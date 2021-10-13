# Serverless Function Compositions

## Initial Setup
Install python package
```
python3 -m venv venv && source ./venv/bin/activate && pip install -e .
```

Install AWS SAM CLI

https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-linux.html#serverless-sam-cli-install-linux-sam-cli

## Building and deploying a composition

### Build
```
sam build
```

### Invoke One Lambda Locally with HTTP
```
sam local api
```

### Invoke One Lambda Locally with CLI
```
sam local invoke <<FunctionName>>
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
Go into one of the composition directories. For example:
```
cd compositions/sync-function-sequence
python3 client.py
```