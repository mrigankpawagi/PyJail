import unittest
import os
from pyjail import Jail

class TestJail(unittest.TestCase):
    def test_add_function(self):
        with Jail() as jail:
            def add(a, b):
                return a + b
            result = jail.execute(add, [1, 2], {})
            self.assertEqual(result, 3)

    def test_divide_function(self):
        with Jail() as jail:
            def divide(a, b):
                return a / b
            with self.assertRaises(ZeroDivisionError):
                jail.execute(divide, [1, 0], {})

    def test_infinite_loop_timeout(self):
        with Jail() as jail:
            def infinite_loop():
                while True:
                    pass
            with self.assertRaises(TimeoutError):
                jail.execute(infinite_loop, [], {}, timeout=1)

    def test_read_file(self):
        with Jail() as jail:
            def read_file():
                with open("/etc/passwd") as f:
                    return f.read()
            with self.assertRaises(Exception):
                jail.execute(read_file, [], {})

    def test_call_os_system(self):
        with Jail() as jail:
            def call_os_system():
                return os.popen("ls /").read()
            with self.assertRaises(Exception):
                jail.execute(call_os_system, [], {})
