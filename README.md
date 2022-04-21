# Async WebSocket Chat
Asynchronous WebSocket Chat allows multiple users to communicate with each other.
This implementation uses Redis Pub/Sub and asynchronous web sockets, and also includes a client.

### Features
- Shows your history after connecting
- Allows you to send messages to any active user


### Endpoints
Endpoint for connecting to websocket:
```
/chat/{user_id}/ws
```

The endpoint that returns the user's history on a GET request
```
/chat/{user_id}/history
```

### Usage

##### Preparation
Create venv:
```bash
make venv
```

Build docker image:
```bash
make docker-build
```

You can run the app without Redis (so it won't work correctly)
```bash
make up
```

##### Running app
Run docker containers (app and redis):
```bash
make docker-run
```

Run client (it will use 'username' as user_id):
```bash
make client
```

You can run client directly and set user_id manually:
```bash
./.venv/bin/python -m client.client your_name
```

##### Client
Send a message to someone:
```bash
@somebody message
```
Note that you should always stick to this format.

Press Enter to exit.


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