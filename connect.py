#!/usr/bin/env python3

import resquests
from requests import ConnectionError
from requests import HTTPError
from requests import Timeout

import logging
logger = logging.getLogger(__name__)

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
