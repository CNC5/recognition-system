import os
from pocketsphinx import LiveSpeech, AudioFile
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


model_path = '/tmp/model_in_ram'
run_path = os.path.abspath('./')

if (not os.path.isdir(model_path)):
    logging.critical('model directory does not exist, terminating')
    quit()
else:
    logging.info('basic checks complete')


speech = AudioFile(
    audio_file=os.path.join(run_path, 'record.wav'),
    verbose=False,
    buffer_size=200,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(model_path, 'zero_ru.cd_cont_4000'),
    lm=os.path.join(model_path, 'ru.lm'),
    dic=os.path.join(model_path, 'ru.dic')
)

logging.info('model loaded')

for chunk in speech:
    print(chunk)