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
import matplotlib.dates as mdates


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


def main():
	hosts = ['capstone0', 'capstone1', 'capstone2']
	types = ['cpu', 'memory', 'disk']
	for host in hosts:
		all_data = get_data(host)
		times  = [data[1] for data in all_data[types[0]]]  
		
		for t in types:
			metric = [data[3] for data in all_data[t]]

			fig, ax = plt.subplots(1)
			fig.autofmt_xdate()
			
			plt.ylabel(t)
			plt.xlabel("Hour")
			plt.plot(times, metric)
			xfmt = mdates.DateFormatter('%H:%M')
			ax.xaxis.set_major_formatter(xfmt)
			plt.savefig(host + '_' + t + '.png')
			plt.gcf().clear()


if __name__ == "__main__":
    main()
