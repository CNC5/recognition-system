# recognition-system
env = pipenv

## install
pipenv install

## usage
### default (localhost-to-localhost)
server: pipenv run python server.py
client: pipenv run python client.py

### custom
server: pipenv run python server.py -d 0.0.0.0 -p <serve_port>
client: pipenv run python client.py -d <server_addr> -p <server_port>

