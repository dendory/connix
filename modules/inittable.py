# Connix - (C) 2016 Patrick Lambert - Provided under the MIT license
# Module inittable - Create tables for other modules to use
from modules import util
import csv
import sys

# Process input
def input(cfg = {}, x = {}):
	cfg['module'] = "InitTable"
	table = util.guid("tmp_")
	if 'table' in x:
		table = x['table']
	try:
		util.debug(cfg, "Mode [" + x['mode'] + "] on table [" + table + "]")
		coldef = ""
		found = False
		for col in x['columns']: # Iterate column config and create column definition
			if found:
				coldef += ", "
			found = True
			coldef += col['name']
			if col['type'] == "number":
				coldef += " INT"
			else:
				coldef += " TEXT"
			if col['primary']:
				coldef += " PRIMARY KEY"
		util.debug(cfg, "Column definition: " + coldef)
		try:
			cfg['db'].execute("SELECT 1 FROM " + table) # If table does not exist, break from 'try'
			if x['mode'] == 'replace' or x['mode'] == 'remove': # If mode is 'replace' or 'remove', drop the table
				cfg['db'].execute("DROP TABLE " + table, [])
				cfg['db'].commit() 
		except:
			if x['mode'] == "create":
				cfg['db'].execute("CREATE TABLE " + table + " (" + coldef + ")", []) # Create the table using column definition
				cfg['db'].commit()		
		if x['mode'] == "replace":
			cfg['db'].execute("CREATE TABLE " + table + " (" + coldef + ")", []) # Create the table using column definition
			cfg['db'].commit()		
	except:
		util.err(cfg, str(sys.exc_info()[1]))
		return False
	cfg['module'] = "Main"
	return True
