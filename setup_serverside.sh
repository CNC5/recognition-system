if [[ ! -e /tmp/model_in_ram ]]; then
	echo 'model RAM folder not found, creating one'
	mkdir /tmp/model_in_ram
	cp -r ./model/* /tmp/model_in_ram
else
	echo 'model folder OK'
fi

if [[ ! -f cert.pem ]] && [[ ! -f key.pem ]]; then
	echo 'no cert and no key files were found, creating default self-signed pair (valid for 365 days)'
	openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365 -nodes
else
	echo 'cert pair OK'
fi
