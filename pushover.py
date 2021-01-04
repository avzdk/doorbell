#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.client
import urllib 
import logging

logger = logging.getLogger(__name__)


class PushOver:
	
	def __init__(self,key,token):
		logger.debug("PushOver Initialized")
		self.key=key
		self.token=token
	
	def send(self,txt,Title='Pi',sound="classical"):
		conn = http.client.HTTPSConnection("api.pushover.net:443")
		conn.request("POST", "/1/messages.json",
		  urllib.parse.urlencode({   
			"token": self.token,
			"user":self.key,
			"message": txt,
			"sound":sound,
			"title":Title
		  }), { "Content-type": "application/x-www-form-urlencoded" })
		return conn.getresponse()