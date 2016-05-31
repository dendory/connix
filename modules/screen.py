# Connix - (C) 2016 Patrick Lambert - Provided under the MIT license
# Screen module - output a specific table to the standard output
from modules import util
import sys

# Process output
def output(cfg = {}, x = {}):
	cfg['module'] = "Screen"
	try:
		util.debug(cfg, "Displaying table [" + x['table'] + "]")
		sql = cfg['db'].cursor()
		sql.execute("SELECT * FROM " + x['table'])
		for row in sql.fetchall():
			print(str(row)) 
	except:
		util.err(cfg, str(sys.exc_info()[1]))
		return False
	return True
