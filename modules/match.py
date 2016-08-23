# Connix - (C) 2016 Patrick Lambert - Provided under the MIT license
# Module sql - parse data with raw SQL queries
from modules import util
import sys

# Process parse
def parse(cfg = {}, x = {}):
	cfg['module'] = "Match"
	try:
		util.debug(cfg, "Querying table [" + x['table'] + "] column [" + x['col'] + "]")
		sql = cfg['db'].cursor()
		sql.execute("SELECT * FROM " + x['table'])
		rows = sql.fetchall()
		headers = [i[0] for i in sql.description]
		util.debug(cfg, "Headers found: " + str(headers))
		colnum = headers.index(x['col'])
		tmp = "CREATE TABLE " + x['newtable'] + " (" # Create statement to be crafted
		qhs = "" # List of headers
		qms = "" # Question marks for the insert statement
		found = False
		colcount = 0
		insertrows = 0
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
			cfg['db'].execute("SELECT 1 FROM " + x['newtable']) # If table does not exist, break from 'try' and create it
			if 'mode' in x:
				if x['mode'] == 'clear': # If mode is 'clear', delete all rows from existing table
					cfg['db'].execute("DELETE FROM " + x['newtable'], [])
					cfg['db'].commit() 
		except:
			cfg['db'].execute(tmp, []) # Create table using crafted statement
			cfg['db'].commit() 
		for row in rows:
			stmt = "INSERT INTO " + x['newtable'] + " (" + qhs + ") VALUES (" + qms + ")"
			if 'mode' in x:
				if x['mode'] == 'merge':
					stmt = "INSERT OR REPLACE INTO " + x['newtable'] + " (" + qhs + ") VALUES (" + qms + ")"
			if 'inverse' in x and x['inverse']: # Inverse match
				if str(x['match']).lower() not in str(row[colnum]).lower():
					cfg['db'].execute(stmt, row)
					insertrows += 1
			else: # Normal match
				if str(x['match']).lower() in str(row[colnum]).lower():
					cfg['db'].execute(stmt, row)
					insertrows += 1
		cfg['db'].commit()
		util.info(cfg, "Wrote " + str(insertrows) + " rows.")
	except:
		util.err(cfg, str(sys.exc_info()[1]))
		return False
	return True
