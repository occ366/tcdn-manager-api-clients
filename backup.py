#!/usr/bin/env python3

import json
import logging
logger = logging.getLogger(__name__)

class Backup:

   def __init__(self,path,list_buckets):

       print('Realizando backup')
       backup_string=''
       logger.info('Starting Backup in: {}'.format(path))

       for bucket in list_buckets:

           backup_string+='\n {} - {}'.format(b.getId(),b.getJson())

       with open(path,'w+') as file:

           file.write(backup_string)
           logger.info('Backup was created in: {} '.format(path))
           print('Backup was created in: {} '.format(path))
