# Connix - (C) 2016 Patrick Lambert - Provided under the MIT license
# Module files - Get a list of files and returns file name and size
from modules import util
import sys
import os

# Process input
def input(cfg = {}, x = {}):
	cfg['module'] = "Files"
	table = util.guid("tmp_")
	if 'table' in x:
		table = x['table']
	try:
		util.debug(cfg, "Listing files from [" + x['folder'] + "] and saving data to table [" + table + "]")
		try:
			cfg['db'].execute("SELECT 1 FROM " + table) # If table does not exist, break from 'try' and create it
			if 'mode' in x:
				if x['mode'] == 'clear': # If mode is 'clear', delete all rows from existing table
					cfg['db'].execute("DELETE FROM " + table, [])
					cfg['db'].commit() 
		except:
			cfg['db'].execute("CREATE TABLE " + table + " (name TEXT, size INT, created INT, modified INT, hash TEXT)", []) # Create table using crafted statement
			cfg['db'].commit()
		rowcount = 0
		for name in os.listdir(x['folder']):
			rowcount += 1
			stmt = "INSERT INTO " + table + " (name, size, created, modified, hash) VALUES (?, ?, ?, ?, ?)"
			if 'mode' in x:
				if x['mode'] == 'merge':
					stmt = "INSERT OR REPLACE INTO " + table + " (name, size, created, modified, hash) VALUES (?, ?, ?, ?, ?)"
			cfg['db'].execute(stmt, [name, os.path.getsize(os.path.join(x['folder'], name)), int(os.path.getctime(os.path.join(x['folder'], name))), int(os.path.getmtime(os.path.join(x['folder'], name))), util.hashfile(os.path.join(x['folder'], name))]) # Append the folder name to file name and get the hash
		cfg['db'].commit()
		util.info(cfg, "Read " + str(rowcount) + " files.")
	except:
		util.err(cfg, str(sys.exc_info()[1]))
		return False
	return True
