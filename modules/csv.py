# Connix - (C) 2016 Patrick Lambert - Provided under the MIT license
# Modules file
from modules import util
import csv
import sys

# Process input
def input(cfg = {}, x = {}):
	cfg['module'] = "CSV"
	stage = util.guid("s_")
	try:
		util.debug(cfg, "Reading file [" + x['file'] + "]")
	except:
		util.err(cfg, "Error parsing module configuration key " + str(sys.exc_info()[1]))
		return False

	try:
		f = open(x['file'], "r")
		util.debug(cfg, "Creating staging table: " + stage)
		cfg['db'].execute("CREATE TABLE " + stage, [])
		cfg['db'].commit() 
		csvreader = csv.reader(f, delimiter=',')
		headers = next(csvreader)
		for header in headers:
			cfg['db'].execute("ALTER TABLE " + stage + "ADD COLUMN ?", [header])
			cfg['db'].commit() 
		rowcount = 0
		for line in csvreader:
			cfg['db'].execute("INSERT INTO " + stage + " VALUES (?, ?)", [line[0], line[1], line[2]])
			cfg['db'].commit()
			rowcount += 1
		util.debug(cfg, "Read " + str(rowcount) + " rows.") 
		f.close()
	except:
		util.err(cfg, str(sys.exc_info()[1]))
		return False


	cfg['module'] = "Main"
	return True
