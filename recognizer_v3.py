import librosa
import time
import string
from espnet2.bin.asr_inference import Speech2Text
import os

fname = 'record.wav'

#checks
if (not os.path.isdir('/tmp/model_in_ram/exp')):
    print('model not found')
    exit()

asr_train_config = '/tmp/model_in_ram/exp/asr_train_asr_conformer_raw_ru_bpe100/config.yaml'
asr_model_file = '/tmp/model_in_ram/exp/asr_train_asr_conformer_raw_ru_bpe100/valid.acc.ave_10best.pth'
model_data = {'asr_train_config':asr_train_config, 'asr_model_file':asr_model_file}

class Recognizer:
    def __init__(self):
        self.speech2text = Speech2Text(
            **model_data,
            device="cpu",
            minlenratio=0.0,
            maxlenratio=0.0,
            ctc_weight=0.3,
            beam_size=10,
            batch_size=0,
            nbest=1
        )

    def load_audio(self, filename):
        audio, sample_rate = librosa.load(filename, sr=44100)
        return audio

    def text_normalizer(self, text):
        text = text.upper()
        return text.translate(str.maketrans('', '', string.punctuation))

    def predict(self):
        speech = self.load_audio(fname)
        nbests = self.speech2text(speech)
        text, *_ = nbests[0]
        return self.text_normalizer(text)

if __name__ == '__main__':
    recg = Recognizer()
    prediction = recg.predict()
    print(prediction)