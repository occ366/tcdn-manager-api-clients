#!/usr/bin/env python3

import json
import logging
logger = logging.getLogger(__name__)

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


