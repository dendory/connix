# Connix - (C) 2016 Patrick Lambert - Provided under the MIT license
# Module ODBC - connect to a databse using a connection string
from modules import util
import pyodbc
import sys

# Process input
def input(cfg = {}, x = {}):
	cfg['module'] = "ODBC"
	table = util.guid("tmp_")
	if 'table' in x:
		table = x['table']
	try:
		util.debug(cfg, "Connecting to [" + x['dsn'] + "] and saving data to table [" + table + "]")
		db = pyodbc.connect(x['dsn'])
		sql = db.cursor()
		sql.execute(x['query'])
		headers = [i[0] for i in sql.description]
		rows = sql.fetchall()
		util.debug(cfg, "Headers found: " + str(headers))
		tmp = "CREATE TABLE " + table + " (" # Create statement to be crafted
		qhs = "" # List of headers
		qms = "" # Question marks for the insert statement
		found = False
		colcount = 0
		for header in headers: # Go through headers and craft create/insert statement
			if found:
				tmp += ", "
				qms += ", "
				qhs += ", "
			found = True
			tmp += header + " TEXT"
			qms += "?"
			qhs += header
			colcount += 1
		tmp += ");"
		try:
			cfg['db'].execute("SELECT 1 FROM " + table) # If table does not exist, break from 'try' and create it
			if 'mode' in x:
				if x['mode'] == 'clear': # If mode is 'clear', delete all rows from existing table
					cfg['db'].execute("DELETE FROM " + table, [])
					cfg['db'].commit() 
		except:
			cfg['db'].execute(tmp, []) # Create table using crafted statement
			cfg['db'].commit() 
		for row in rows:
			stmt = "INSERT INTO " + table + " (" + qhs + ") VALUES (" + qms + ")"
			if 'mode' in x:
				if x['mode'] == 'merge':
					stmt = "INSERT OR REPLACE INTO " + table + " (" + qhs + ") VALUES (" + qms + ")"
			cfg['db'].execute(stmt, row)
		cfg['db'].commit()
		db.close()
		util.info(cfg, "Read " + str(len(headers)) + " columns, " + str(len(rows)) + " rows.")
	except:
		util.err(cfg, str(sys.exc_info()[1]))
		return False
	return True

# Process output
def output(cfg = {}, x = {}):
	cfg['module'] = "ODBC"
	odbctable = util.guid("tmp_")
	if 'odbctable' in x:
		odbctable = x['odbctable']
	try:
		util.debug(cfg, "Connecting to [" + x['dsn'] + "]")
		db = pyodbc.connect(x['dsn'])
		util.debug(cfg, "Writing table [" + x['table'] + "] to ODBC table [" + odbctable + "]")
		tmp = "CREATE TABLE " + odbctable + " (" # Create statement to be crafted
		qhs = "" # List of headers
		qms = "" # Question marks for the insert statement
		found = False
		sql = cfg['db'].cursor()
		sql.execute("SELECT * FROM " + x['table'])
		for header in [i[0] for i in sql.description]: # Go through headers and craft create/insert statement
			if found:
				tmp += ", "
				qms += ", "
				qhs += ", "
			found = True
			tmp += header + " VARCHAR(MAX)"
			qms += "?"
			qhs += header
		tmp += ");"
		try:
			db.execute("SELECT 1 FROM " + odbctable) # If table does not exist, break from 'try' and create it
			if 'mode' in x:
				if x['mode'] == 'clear': # If mode is 'clear', delete all rows from existing table
					db.execute("DELETE FROM " + odbctable, [])
					db.commit() 
		except:
			db.execute(tmp, []) # Create table using crafted statement
			db.commit() 
		rows = sql.fetchall()
		for row in rows:
			stmt = "INSERT INTO " + odbctable + " (" + qhs + ") VALUES (" + qms + ")"
			if 'mode' in x:
				if x['mode'] == 'merge':
					stmt = "INSERT OR REPLACE INTO " + odbctable + " (" + qhs + ") VALUES (" + qms + ")"
			db.execute(stmt, row)
		db.commit()
		util.info(cfg, "Wrote " + str(len(rows)) + " rows.")
		db.close()
	except:
		util.err(cfg, str(sys.exc_info()[1]))
		return False
	return True
