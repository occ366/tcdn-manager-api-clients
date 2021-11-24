#!/usr/bin/python
import sys
sys.path.append('/opt/p2pcdn/lib/entrypoint/')
import datetime
import logging
from logging import FileHandler
from logging import Formatter
import getpass
import requests
from requests import ConnectionError
from requests import HTTPError
from requests import Timeout
import json
import time


FILE_BACKUP = '/tmp/backups_api_buckets_'+str(datetime.date.today())
DEBUG_LOG_PATH='/tmp/log_api_operaction.log'
URL_MGR='http://127.0.0.1:8082/api/v4/buckets/'
DEBUG_LOG_FORMAT = ("%(asctime)s [%(levelname)s]: %(message)s")
TIME_OUT=10
TIME_DELAY=0.5
BUCKET_TEST=1

logger = logging.getLogger('debug')
logger.setLevel(logging.DEBUG)
logger_file_handler = FileHandler(DEBUG_LOG_PATH)
logger_file_handler.setLevel(logging.DEBUG)
logger_file_handler.setFormatter(Formatter(DEBUG_LOG_FORMAT))
logger.addHandler(logger_file_handler)


#class for api connections

class Connect:
    
    def __init__(self, user, pwd): 
        self.__auth=(user,pwd)
    			
    def get_auth(self):
        return self.__auth
	
    def set_auth(self,user,pwd):
        self.__auth = (user,pwd) 
	
    def put(self,url,json):
        try:
            response=requests.put(url,auth=self.__auth,data=json.dumps(json))
            response.raise_for_status()
            logger.info('connect.put(): put json for: {}'.format(url))

            return response

            except ConnectionError:
                logger.info('Connection error. Retrying...')
                sleep(TIME_OUT)

            except Timeout:
                logger.info('Timeout. Retrying...')
                sleep(TIME_OUT)

            except HTTPError:
                logger.error('HTTP error. Code {}'.format(set))

            except:
                logger.info('Unexpected error {}'.format(set))
    
    def get(self,url):
        try:
            response=requests.get(url,auth=self.__auth)
            response.raise_for_status()
            logger.info('Get Json for: {}'.format(url))
            return response

        except ConnectionError:
            logger.info('Connection error. Retrying...')

        except Timeout:
            logger.info('Timeout. Retrying...')
            sleep(TIME_OUT)

        except HTTPError:
            logger.error('HTTP error. Code {}'.format(set))
         
        except:
            logger.info('Unexpected error {}'.format(set))

    def check_auth(self,url):

        auth=resquests.get(url,auth=self.__auth)

        if '401' in str(auth.status_response):
            logger.error('Wrong user or password')
            print('Wrong user or password')
            return False
        else:
            logger.info('login sucessful with user: '+ str(self.__auth[0]))
            return True

#class for buckets

class Bucket:

    def __init__(self, id, type, connect ):

        self.__id = id
        self.__type = type
        self.__bucket_url= '{}/{}/{}'.format(URL_MGR,type,id)
        self.__json = connect.get(bucket_url).json()
        self.__secrets = self.__json["overflow_config"]["akamai_secrets"]

    def getId(self):

        return self.__id

   def getJson():

       return self.__json

   def checkHasSecret(self,csecrets):

       newSecrets=self.__json["overflow_config"]["akamai_secrets"]
       
       try:
           for csecrest in csecrets:
               for secret in self.__json["overflow_config"]["akamai_secrets"]:
                   if csecret["secret"] in secret["secret"]:
                      logger.info('bucket.checkHasSecret(): bucket {} have configurate secret: {}'.format(self.__id, secret["secret"]))
                   
                  else:
                      newSecrects.append(csecret)
                      logger.info('bucket.checkHasSecret(): new secret add to bucket: {}'.format(self.__id, secret["secret"]))

        except:
            logger.info('bucket.checkHasSecret(): Not secrets configs')
        
        return 

    def updateSecrets(self, connect, csecrets):

        json_secrets=self.checkHasSecret(csecrets)

        if (self.__json["hosts"] in "\.") and json_secrests):


            host = ".edgesuite.net".format(self.__json["hosts"])
            newjson={"overflow_config": {"type": 2,"status": 0,"percentage": 100,"host": host ,"akamai_secrets": [json_secrests]}}
            
            connect.put(self.__url,json.dump(newjson))



#class for made a backup

class Backup:

   def __init__(self,path,list_buckets):

       print('Realizando backup')
       backup_string=''
       logger.info('Starting Backup in: {}'.format(path))

       for bucket in list_buckets:

           backup_string+='\n {} - {}'.format(b.getId(),b.getJson()

       with open(path,'w+') as file:

           file.write(backup_string)
           logger.info('Backup was created in: {} '.format(path))
           print('Backup was created in: {} '.format(path))


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

    

def main():

    #Get inputs
    
    USER =  getpass.getpass('--> User for API:')
    PWD = getpass.getpass('--> Password for API:')

    json_path = str(input('--> Type path for json file: '))
    bucket_path = str(input('--> Type path for buckets file: '))
    type_buckets = str(input('--> Type bucekts (vod, live, or webcache): '))

    connect = Connect(USER,PWD)
    url= '{}/{}/{}'.format(URL_MGR,'vod','1')

    try:

        connect.check_auth(url):

        json_path = str(input('--> Type path for json file: '))
        bucket_path = str(input('--> Type path for buckets file: '))
        type_buckets = str(input('--> Type bucekts (vod, live, or webcache): '))

        bucket_path = str(input('--> Type path for buckets file: '))
        list_buckets = data_input.buckets(connect,type)
        list_secrets = data_input.secrets()
	backup=Backup(FILE_BACKUP,list_buckets)
			
	logger.info('.........Starting script...........')
        for bucket in list_buckets:

            logger.info('Updating settings on bucket: {}'.format(bucket.getId()))
            print('Update the json on bucket: {}'.format(bucket.getId()))
	    logger.info('Update the json {} on bucket: {}'.format(list_secrets,bucket.getId()))
	    bucket.updateSecrets(connect,list_secrets)
            time.sleep(TIME_DELAY)
            logger.info('End of the Change.... ')
	    print('End of the changes, check execution in: {}'.format(DEBUG_LOG_PATH))

    except:
	print('Problem with the execution, check '.format(DEBUG_LOG_PATH))

if __name_ == __main__:

    main()
