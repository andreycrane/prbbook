#!/usr/bin/env python
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import codecs
from itertools import izip

class HtmlStudentsParser(HTMLParser, object):
	def __init__(self, text, *args, **kwargs):
		super(HtmlStudentsParser, self).__init__(*args, **kwargs)
		self.add = False
		self.data = []
		self.feed(text)

	def handle_starttag(self, tag, attrs):
		if tag == 'td':
			self.add = True
		else:
			self.add = False
	
	def handle_endtag(self, tag):
		if tag == 'td':
			self.add = False

	def handle_data(self, data):
		if self.add:
			self.data.append(unicode(data))

	def get_list(self):
		return list(izip(*(iter(self.data[4:]),) * 4))

class CsvStudentsParser(object):
	def __init__(self, text):
		lines = text.splitlines()[1:]
		self.list = []
		for line in lines:
			columns = line.split(';')
			self.list.append((columns[0], columns[2].split('-')[-1], columns[3], columns[7]))

	def get_list(self):
		return self.list