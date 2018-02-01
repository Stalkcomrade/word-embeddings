#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 13:54:10 2018

@author: stlk
"""

import argparse
# Define the parser
parser = argparse.ArgumentParser(description='Short sample app')
# Declare an argument (`--algo`), telling that the corresponding value should be stored in the `algo` field, and using a default value if the argument isn't given
parser.add_argument('--words', action="store", dest='words', default=500)
parser.add_argument('--clusters', action="store", dest='clusters', default=10)
# Now, parse the command line arguments and store the values in the `args` variable
args = parser.parse_args()
# Individual arguments can be accessed as attributes...
print(args.clusters)

import platform
print(platform.python_version())