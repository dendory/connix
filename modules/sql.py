# Connix - (C) 2016 Patrick Lambert - Provided under the MIT license
# Module sql - parse data with raw SQL queries
from modules import util
import sys

# Process parse
def parse(cfg = {}, x = {}):
	cfg['module'] = "SQL"
	try:
		util.debug(cfg, "Query [" + x['query'] + "]")
		a = cfg['db'].execute(x['query'])
		cfg['db'].commit()
		util.info(cfg, str(a.rowcount) + " rows affected.")		
	except:
		util.err(cfg, str(sys.exc_info()[1]))
		return False
	return True
