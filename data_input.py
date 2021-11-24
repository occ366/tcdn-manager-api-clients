#!/usr/bin/env python3

import json
import logging
logger = logging.getLogger(__name__)

class Data_input:

    def __init__(self,path_json_file,path_buckets_file):

        self.__path_json = path_json_file
        self.__path_bucket_file = path_buckets_file

    def secrets(self):

        try:
            with open(path_json_file) as file:
                 for line in file:
                    self.__listNewSecrets.append(json.dumps(line))

            logger.info('Data_input.secrets(): Load secrest lists on file: '.format(path_secrets_json_file))
            return self.__listNewSecrets

        except FileNotFoundError:
        logger.error('Data_input.secrets(): File doesnt {} exist'.format(path_secrets_json_file))


    def buckets(self,connect,type):

        try:
            with open(path_bucket_file) as file:
                for line in file:
                    self.__list_buckets.append(Bucket(str(line), type, connect)))

            return self.__list_buckets
            logger.info('Data_input.secrets(): Load bucket lists on file: '.format(path_secrets_json_file))

        except FileNotFoundError:
            logger.error('Data_input.buckets(): File doesnt {} exist'.format(path_secrets_json_file))
