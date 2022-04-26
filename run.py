#!/usr/bin/env python3

import importlib.util
import sys

spec = importlib.util.spec_from_file_location('mymodule', 'module.py')
mymodule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mymodule)

mymodule.funcA()
mymodule.funcB()
