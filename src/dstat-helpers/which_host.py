#!/usr/bin/python
import pytoml as toml
import psycopg2
import sys

# given a key {'cpu', 'memory', 'disk'}, returns the average
# of that value from the last 'number' of rows
def get_avg(key, rows, number):
        list_of_trait_with_key = [x[3] for x in rows[:number] if key in x]
	return reduce(lambda x, y: x + y, list_of_trait_with_key) / len(list_of_trait_with_key)
	
def get_averages(num_rows):
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
		host = 'localhost'
		conn_str = "dbname='stats' user=" + username + " host=" + host + " password=" + password
		print(conn_str)
		conn = psycopg2.connect(conn_str)
	except:
		print "Unexpected error:", sys.exc_info()[0]

	# get cursor
	cur = conn.cursor()

	# get and print rows
	cur.execute("""SELECT * from metrics""")
	rows = cur.fetchall()
	for i in range(num_rows):
		print str(rows[i])

	# compute averages
	disk = get_avg('disk', rows, num_rows)
	cpu = get_avg('cpu', rows, num_rows)
	memory = get_avg('memory', rows, num_rows)

	return {'disk': disk, 'cpu':cpu, 'memory':memory}


num_rows = 100
print "average over last {} rows: {}".format(num_rows, get_averages(num_rows))
