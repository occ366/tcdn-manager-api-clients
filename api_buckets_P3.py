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

class FileNotFoundError(OSError):
    pass

#load of json files
class load_file_json:
	def __init__(self):
		self.__path = str(input('--> Type path for json file: '))
 				
	def get(self):
		try:
			f=open(self.__path, "r")
			json=f.read()
			f.close()
			return json
		except FileNotFoundError:
			logger.error('file '+ str(self.__path) + 'doesnt exist')
	
#class for api connections

class Api_bucket:
	def __init__(self, user, pwd): 
		self.__auth=(user,pwd)
		
				
	def get_auth(self):
       		 return self.__auth
	
	def set_auth(self,user,pwd):
        	self.__auth = (user,pwd) 
	
	def set_json(self,url,json):
			try:
					set=requests.put(url,auth=self.__auth,data=json.get())
					set.raise_for_status()
					logger.info('Put json for:'+ url)
								
			except ConnectionError:
					logger.info('Connection error. Retrying...')
					sleep(TIME_OUT)
			except Timeout:
					logger.info('Timeout. Retrying...')
					sleep(TIME_OUT)
			except HTTPError:
					logger.error('HTTP error. Code' + str(set))
			except:
					logger.info('Unexpected error'+ str(set))
					
	def get_json(self,url):
			try:
					get=requests.get(url,auth=self.__auth)
					get.raise_for_status()
					logger.info('Get Json for: '+ url)
					return get.json()
			except ConnectionError:
					logger.info('Connection error. Retrying...')
					sleep(TIME_OUT)
			except Timeout:
					logger.info('Timeout. Retrying...')
					sleep(TIME_OUT)
			except HTTPError:
					logger.info('HTTP error. Code: '+ str(get))
			except:
					logger.info('Unexpected error')

	def check_auth(self,url):
		auth_json=requests.get(url,auth=self.__auth)
		if '401' in str(auth_json):
			logger.error('Wrong user or password')
			print('Wrong user or password')
			return False
		else: 
			logger.info('login sucessful with user: '+ str(self.__auth[0]))
			return True

#class for buckets
class Bucket:
	def __init__(self, id, type):
		self.__id = id
		self.__type=type
	def get_id(self):
		return self.__id
	def get_type(self):
		return self.__type
		
	def set_id(self,id):
		self.__id = id
	def set_type(self,type):
		self.__type = type

#class for made a backup
class Backup:
	def __init__(self,path,list_buckets,api_bucket):
		print('Realizando backup')
		backup_string=''
		logger.info('Starting Backup in: '+path)
		for b in list_buckets:
			url=URL_MGR+str(b.get_type())+'/'+str(b.get_id())
			json = api_bucket.get_json(url)
			backup_string+='\n'+str(b.get_id())+' - '+ str(json)
		with open(path,'w+') as file:
			file.write(backup_string)
		logger.info('Backup was created in: '+path)
		print('Backup was created in: '+path)
def main():

	#Get Credenciales
	
	bucket = Bucket(BUCKET_TEST,'vod')
	USER =  getpass.getpass('--> User for API:')
	PWD = getpass.getpass('--> Password for API:')
	url=URL_MGR+str(bucket.get_type())+'/'+str(bucket.get_id())
	api_bucket = Api_bucket(USER,PWD)
	if api_bucket.check_auth(url):
		json=load_file_json()
		list_buckets=[]
		type_buckets = str(input('--> Type bucekts (vod, live, or webcache): '))
		file_buckets = str(input('--> Path to bucket lists: '))
		logger.info('Try to load bucket lists on file: '+ str(file_buckets))
		try:
			with open(file_buckets) as flist:
				for line in flist:
					list_buckets.append(Bucket(str(line.strip()),type_buckets))
		except IOError:
			logger.error('file '+ str(file_buckets) + 'doesnt exist')
		logger.info('.........Starting script...........')
		backup=Backup(FILE_BACKUP,list_buckets,api_bucket)
		for b in list_buckets:
			url=URL_MGR+str(b.get_type())+'/'+str(b.get_id())
			logger.info('Updating settings on bucket: '+ str(b.get_id()))
			print('Update the json on bucket: '+str(b.get_id()))
			logger.info('Update the json '+ str(json.get()) +' on bucket: '+str(b.get_id()))
			api_bucket.set_json(url,json)	
			time.sleep(TIME_DELAY)
		logger.info('End of the Change.... ')
		print('End of the changes, check execution in: ' + DEBUG_LOG_PATH)
	else:
		print('Problem with the execution, check ' + DEBUG_LOG_PATH)
	
main()
