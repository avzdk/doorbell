#!/usr/bin/env python3


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
import time
import configparser
import logging
from pushover import PushOver

conf = configparser.ConfigParser()
conf.read(['doorbell.ini','doorbell_local.ini'])

pushover=PushOver(conf['Pushover']['Key'], conf['Pushover']['Token'])		

log = logging.getLogger(__name__)
logging.basicConfig(
    level=conf["LOG"]["LEVEL"],
    format="%(levelname)s %(module)s.%(funcName)s %(message)s",
)
log.info(f"Starting service loglevel={conf['LOG']['LEVEL']} ")


class Doorbell:
	def __init__(self):
		self.last_pressed=time.time()
		GPIO.setup(7, GPIO.IN)
		self.stateChangeTime=time.time()
	
	def check_knap(self):
		while True:
			log.debug("venter")
			edge=GPIO.wait_for_edge(7, GPIO.RISING)
			time.sleep(0.005) # debounce for 5mSec
            # only show valid edges
			if GPIO.input(7) == 1:
				log.debug("True Rising")
				last_stateChangeTime=self.stateChangeTime  
				self.stateChangeTime=time.time()
				log.debug("Ringklokke trykket" " efter " + str(self.stateChangeTime-last_stateChangeTime))	
				self.tryk(0)
			else:
				log.debug("False Rising")


			
	def tryk(self,tryktid):
		if time.time()-self.last_pressed > 5:  # kun et tryk pr 5 sekunder
			log.info("Ringklokke trykket")
			rv = pushover.send(conf['Pushover']['MessageBody'],conf['Pushover']['MessageTitle'])
			log.debug(rv)
		self.last_pressed=time.time()


		
def main():
    doorbell=Doorbell()
    doorbell.check_knap()

if __name__ == "__main__":
    main()


			


