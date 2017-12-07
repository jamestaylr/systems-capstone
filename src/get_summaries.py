#!/usr/bin/env python
import os_client_config
import requests
import json
import pytoml as toml
import psycopg2
import sys
import datetime
import numpy as np
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def get_data(hostname):
	# parse config
	file_name = "/usr/local/dstat/config.toml"
	with open(file_name, 'rb') as fin:
		obj = toml.load(fin)
	print obj


	# connect to database
	try:
		database = obj['database']
		username = database['user']
		password = database['password']
		host = database['host']
		conn_str = "dbname='stats' user=" + username + " host=" + host + " password=" + password
		print(conn_str)
		conn = psycopg2.connect(conn_str)
	except:
		print "Unexpected error:", sys.exc_info()[0]

	# get cursor
	cur = conn.cursor()

	# get and print rows
	now = datetime.datetime.now()
	d = now.strftime("%Y-%m-%d")
	
	types = ["cpu", "memory", "disk"]
	data = {}
	for t in types:

		query = "SELECT * from metrics WHERE datetime ::date >= to_date('{}' ,'YYYY-MM-DD') and datetime::date <= to_date('{}','YYYY-MM-DD') AND hostname = '{}' and type = '{}'".format(d, d,hostname, t)
		cur.execute(query)
		rows = cur.fetchall()
		data[t] = rows
	
	return data

def calculate_pressure(data):
    for host, metrics in data.items():
        for metric, h in metrics.items():
            data[host][metric]['pressure'] = h['expected'] / h['constant']
            logging.info('[{}] Metric {} at {} threshold'.format(
                host,
                metric,
                data[host][metric]['pressure']
            ))
    return data


def main():
    cap0 = get_data('capstone0')
    times  = [data[1] for data in cap0['cpu']]  
    cpus = [data[3] for data in cap0['cpu']]
    memories = [data[3] for data in cap0['memory']]
    disks = [data[3] for data in cap0['disk']]
    plt.plot(times, cpus)
    plt.savefig('cap0.png')
if __name__ == "__main__":
    main()
