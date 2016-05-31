# Connix - (C) 2016 Patrick Lambert - Provided under the MIT license
# Module sql - parse data with raw SQL queries
from modules import util
import sys

# Process parse
def parse(cfg = {}, x = {}):
	cfg['module'] = "SQL"
	try:
		util.debug(cfg, "Query [" + x['query'] + "]")
		cfg['db'].execute(x['query'])
		cfg['db'].commit()		
	except:
		util.err(cfg, str(sys.exc_info()[1]))
		return False
	return True
