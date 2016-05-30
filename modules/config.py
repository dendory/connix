# Connix - (C) 2016 Patrick Lambert - Provided under the MIT license
# Configuration parsing
import sys
import json

def read_config(file = "connix.cfg"):
	ret = {'status': False, 'file': file, 'json': None, 'result': ""}
	try:
		f = open(file, "r")
		ret['json'] = json.loads(f.read())
		f.close()
		ret['status'] = True
	except:
		ret['result'] = str(sys.exc_info()[1])
	return ret
