# -*- coding: utf-8 -*-
"""
Site tools test related stuff module
====================================

.. module:: sitetools.test
    :platform: Django
    :synopsis: Site tools test related stuff module
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Python imports
import json

# Django imports
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

class EnhancedTestCase(TestCase):
	"""
	Enhanced test case class
	"""
	client=Client()

	def post(self,viewname,postdata):
		"""
		Emulate a post request to given view
		"""
		return self.client.post(reverse(viewname),postdata)

	def get(self,viewname):
		"""
		Emulate a post request to given view
		"""
		return self.client.get(reverse(viewname))

	def json_post(self,viewname,postdata):
		"""
		Emulate a post request to given json view 
		"""
		return json.loads(self.post(viewname,postdata).content)

	def json_get(self,viewname):
		"""
		Emulate a post request to given json view
		"""
		return json.loads(self.get(viewname).content)
