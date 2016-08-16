# Connix - (C) 2016 Patrick Lambert - Provided under the MIT license
# Module sql - parse data with raw SQL queries
from modules import util
import sys

# Process parse
def parse(cfg = {}, x = {}):
	cfg['module'] = "SQL"
	table = util.guid("tmp_")
	if 'table' in x:
		table = x['table']
	try:
		util.debug(cfg, "Query [" + x['query'] + "]")
		if 'type' in x and 'sel' in x['type']: # Select query
			sql = cfg['db'].cursor()
			sql.execute(x['query'])
			headers = [i[0] for i in sql.description]
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
			sql = cfg['db'].cursor()
			sql.execute(x['query'])
			rows = sql.fetchall()
			for row in rows:
				stmt = "INSERT INTO " + table + " (" + qhs + ") VALUES (" + qms + ")"
				if 'mode' in x:
					if x['mode'] == 'merge':
						stmt = "INSERT OR REPLACE INTO " + table + " (" + qhs + ") VALUES (" + qms + ")"
				cfg['db'].execute(stmt, row)
			cfg['db'].commit()
			util.info(cfg, "Wrote " + str(len(rows)) + " rows.")
		else: # Non-select query
			a = cfg['db'].execute(x['query'])
			cfg['db'].commit()
			util.info(cfg, str(a.rowcount) + " rows affected.")		
	except:
		util.err(cfg, str(sys.exc_info()[1]))
		return False
	return True
