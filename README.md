# Serverless Function Compositions

## Initial Setup

```
python3 -m venv venv && source ./venv/bin/activate && pip install -e .
```


## Building and deploying a composition

### Build
```
sam build
```

### Invoke Locally with HTTP
```
sam local api
```

### Invoke Locally with CLI
```
sam local invoke <<FunctionName>>
```


### Deployment
First time
```
sam deploy --guided
```

With `samconfig.toml` saved in root dir
```
sam deploy
```