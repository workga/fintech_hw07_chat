# Image Resizer
API that allows you to scale images.

### Features
- Using Redis to store images and tasks
- Using python-rq for task queue
- Three docker containers for application, Redis and workers


### Endpoints
You can see API documentation in swagger using url:
```
/docs
```

### Usage

Create venv:
```bash
    make venv
```

Run application:
```bash
    make up
```

Build docker image:
```bash
make docker-build
```

Run docker containers:
```bash
make docker-run
```

### Development
Run tests:
```bash
    make test
```

Run linters:
```bash
    make lint
```

Run formatters:
```bash
    make format
```