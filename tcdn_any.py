#!/usr/bin/env python3

import sys

import datetime
import getpass
import json
import time
import logging
from buckets import Bucket
from connect import Connect
from data_input import Data_input


global logger

sys.path.append('/opt/p2pcdn/lib/entrypoint/')

FILE_BACKUP = '/tmp/backups_api_buckets_'+str(datetime.date.today())
LOG_PATH='/tmp/log_api_changes_overflow.log'
URL_MGR='http://127.0.0.1:8082/api/v4/buckets/'
LOG_FORMAT = ("%(asctime)s [%(levelname)s]: %(message)s")

TIME_OUT=10
TIME_DELAY=0.5
BUCKET_TEST=1

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.FileHandler(LOG_PATH)
logger_file_handler.setLevel(logging.DEBUG)
logger_file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(logger_file_handler)


def main():

    USER =  getpass.getpass('--> User for API:')
    PWD = getpass.getpass('--> Password for API:')

    json_path = str(input('--> Type path for json file: '))
    bucket_path = str(input('--> Type path for buckets file: '))
    type_buckets = str(input('--> Type bucekts (vod, live, or webcache): '))

    connect = Connect(USER,PWD)
    url= '{}/{}/{}'.format(URL_MGR,'vod','1')

    try:

        connect.check_auth(url)

        json_path = str(input('--> Type path for json file: '))
        bucket_path = str(input('--> Type path for buckets file: '))
        type_buckets = str(input('--> Type bucekts (vod, live, or webcache): '))

        bucket_path = str(input('--> Type path for buckets file: '))
        list_buckets = data_input.buckets(connect,type)
        json_load = data_input.json()
        backup=Backup(FILE_BACKUP,list_buckets)

        logger.info('.........Starting script...........')
        for bucket in list_buckets:

            logger.info('Updating settings on bucket: {}'.format(bucket.getId()))
            print('Update the json on bucket: {}'.format(bucket.getId()))
            logger.info('Update the json {} on bucket: {}'.format(json_load,bucket.getId()))
            bucket.updateJson(connect,json_list)
            time.sleep(TIME_DELAY)
            logger.info('End of the Change.... ')
            print('End of the changes, check execution in: {}'.format(LOG_PATH))

    except:
        print('Problem with the execution, check '.format(LOG_PATH))

if __name__ == "__main__":

    main()
