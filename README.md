# recognition-system
env = pipenv

## install
pipenv install

## usage
### prep
bash setup_serverside.sh

### default (localhost-to-localhost)
server:
	pipenv run python server.py<br>

client:
	pipenv run python client.py

### custom
server:
	pipenv run python server.py -d 0.0.0.0 -p <serve_port><br>

client:
	pipenv run python client.py -d <server_addr> -p <server_port>
