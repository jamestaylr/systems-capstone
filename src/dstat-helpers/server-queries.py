"""
An untested file.
A skeleton for queries on the dstat server
versus using a database query directly.
"""

import requests
import pytoml as toml

# parse config
file_name = "/usr/local/dstat/config.toml"
with open(file_name, 'rb') as fin:
	obj = toml.load(fin)
print obj

# set up port
port = obj['daemon']['port']
connecting_to = 'http://localhost:' + str(port)

# connect to server
print("now we are connecting to: " + connecting_to)
requests.get(connecting_to)
