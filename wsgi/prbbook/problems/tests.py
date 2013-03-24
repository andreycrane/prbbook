#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from prbbook import settings
from models import Problem
from prbbook.engines.engine_1 import ProblemEngine

class EngineTest(TestCase):
    # выполняем настройку теста
    def setUp(self):
        self.engine = ProblemEngine()
        self.engine.load_preview_params()

    # завершающие действия
    def tearDown(self):
        pass

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_get_store_str(self):
        dump_str = self.engine.get_store_str()
        test_str = '{"h2": 9.0, "h1": 13.0, "b1": 11.0, "b2": 4.0, "y0": 1.0, "z0": 1.0}'
        self.assertEqual(dump_str, test_str)
        self.dump_str = dump_str

    def test_load_store_str(self):
        load_str = '{"h2": %.1f, "h1": %.1f, "b1": %.1f, "b2": %.1f, "y0": %.1f, "z0": %.1f}' % (1, 1, 1, 1, 1, 1)
        self.engine.load_store_str(load_str)
        dump_str = self.engine.get_store_str()
        self.assertEqual(load_str, dump_str)