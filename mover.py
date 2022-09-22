import os
import configparser

config = configparser.ConfigParser()
conf_name = 'schedule.ini'
config.read(conf_name)
contents = os.listdir()
for filename in contents:
	if 'record_' in filename:
		r_type, r_time, r_date = filename.split('_')
		r_hour, r_min, r_sec = r_time.split(':')
		