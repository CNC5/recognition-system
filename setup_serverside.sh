echo 'checks:'

if [ '$(uname -m)' != 'amd64' ]; then
	echo 'arch '$(uname -m)' is not supported'
	exit 1
fi

if [[ ! -e /tmp/model_in_ram ]]; then
	echo 'model RAM folder not found, creating one'
	mkdir /tmp/model_in_ram
else
	echo 'OK'
fi

if [[ ! -e exp ]]; then
	if [[ ! -f asr_train_asr_conformer_raw_ru_bpe100_valid.acc.ave.zip ]]; then
		echo 'no model or model archive was found, downloading and unpacking'
		wget https://zenodo.org/record/4541727/files/asr_train_asr_conformer_raw_ru_bpe100_valid.acc.ave.zip?download=1 && mv asr_train_asr_conformer_raw_ru_bpe100_valid.acc.ave.zip?download=1 asr_train_asr_conformer_raw_ru_bpe100_valid.acc.ave.zip && unzip asr_train_asr_conformer_raw_ru_bpe100_valid.acc.ave.zip
	else
		echo 'no model was found but a model archive is present, unpacking'
		unzip asr_train_asr_conformer_raw_ru_bpe100_valid.acc.ave.zip
	fi
else
	echo 'OK'
fi

if [[ ! -e /tmp/model_in_ram/exp ]]; then
	if [[ -e exp ]]; then
		mv exp /tmp/model_in_ram
		echo 'model loaded'
	else
		echo 'no model to load to RAM, terminating'
		exit 1
	fi
else
	echo 'model already loaded'
fi

if [[ ! -f cert.pem ]] && [[ ! -f key.pem ]]; then
	echo 'no cert and no key files were found, creating default self-signed pair (valid for 365 days)'
	openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365 -nodes
else
	echo 'OK'
fi
