#!/usr/bin/env python
# -*- coding: utf-8 -*-
from termcolor import colored
import traceback

class TestFailedError(Exception):
    def __init__(self, *args, **kwargs):
        super(TestFailedError, self).__init__(*args, **kwargs)

class EngineTest:
    # количество прогонов тестирования движка
    runs = 10
    # класс задачи
    engine = None

    def __init__(self):
        # в данной переменной хранятся расчитанные параметры задачи
        # используются тестами для утверждений
        self.params = None
        # массив с данными каждого отельного прогона
        self.runs_data = []
        # номер текущего прогона тестов
        self.current_run = None

    # вызывает исключение если утверждение равно
    def assertEqual(self, a, b, msg = u"Утверждение Equal верно!"):
        if a == b:
            raise TestFailedError(msg)

    def assertNotEqual(self, a, b, msg = u"Утверждение NotEqaul верно!"):
        if a != b:
            raise TestFailedError(msg)

    def call_tests(self):
        # создаем список атрибутов потенциальных функций тестов
        tests = [test for test in dir(self) if test.startswith("test_")]
        self.runs_data[self.current_run]['test_count'] = len(tests)
        # вызываем каждый тест если таковой вызываемый
        for test in tests:
            test_func = getattr(self, test)
            if callable(test_func):
                try:
                    test_func()
                except TestFailedError as e:
                    self.runs_data[self.current_run]['failed_tests'].append(u"Тест %s провален: %s" % (test, e.message))
                except Exception as e:
                    self.runs_data[self.current_run]['error_tests'].append(traceback.format_exc())
                else:
                    self.runs_data[self.current_run]['passed_tests'].append("Test %s passed" % test)

    def run(self):
        print colored(u"Выполняю прогоны тестов")
        for i in xrange(self.__class__.runs):
            # создаем хеш с данными прогона
            self.runs_data.append({'runs': 0, 
                    'generation_errors': [],
                    'test_count': 0,
                    'failed_tests': [],
                    'error_tests': [],
                    'passed_tests': []})

            self.current_run = i
            # цикл генерирования
            generation_count = 0 # количество циклов генерирования
            while True:
                generation_count += 1
                try:
                    # извлекаем класс задачи
                    Engine = self.__class__.engine
                    # инстанцируем класс
                    engine = Engine()
                    # генерируем исходные данные
                    engine.randomize_in_params()
                    # выполняем корректировку
                    engine.adjust()
                    # выполняем расчет задачи
                    self.params = engine.calculate()
                except Exception as e:
                    self.runs_data[i]['generation_errors'].append(traceback.format_exc())
                else:
                    # сохраняем в данных прогона количество циклов генерирования
                    self.runs_data[i]['runs'] = generation_count
                    self.call_tests()
                    break
            print colored("#", "green"),
        print "\n"
        runs_with_failed = 0
        runs_with_errors = 0
        runs_with_generation_errors = 0
        # выводим информацию по тестированию в кажлом отдельном прогоне
        for (i, run_data) in enumerate(self.runs_data):
            print colored(u"--- Прогон #%d ---" % (i + 1), "green")
            print u"Количество циклов генерирования: %d" % run_data['runs']
            if run_data['generation_errors']:
                runs_with_generation_errors += 1
                print colored(u"Ошибки при генерировании: ", "red")
                for e in run_data['generation_errors']:
                    print "---------------------------"
                    print e
                    print "---------------------------"
            print u"Тестов всего: %d" % run_data['test_count']
            print colored(u"Тестов пройдено: %d" % len(run_data['passed_tests']), "green")
            print colored(u"Тестов не пройдено: %d" % len(run_data['failed_tests']), "yellow")
            if run_data['failed_tests']:
                runs_with_failed += 1
            for failed_test in run_data['failed_tests']:
                print "-------------------------------"
                print failed_test
                print "-------------------------------"
            print colored(u"Ошибки при выполнении тестов: %d" % len(run_data['error_tests']), "red")
            if run_data['error_tests']:
                runs_with_errors += 1
            for error_test in run_data['error_tests']:
                print "-------------------------------"
                print error_test
                print "-------------------------------"
            print "\n"
        # выводим информацию по прогонам в целом
        print "----------- Итог тестирования --------------------"
        print u"Количество прогонов с ошибками генерирования: %d" % runs_with_generation_errors
        print u"Количество прогонов с провальными тестами: %d" % runs_with_failed
        print u"Количество прогонов с ошибочным выполнением: %d" % runs_with_errors