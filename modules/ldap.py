# Connix - (C) 2016 Patrick Lambert - Provided under the MIT license
# Module ODBC - connect to a databse using a connection string
from modules import util
import sys

# Process input
def input(cfg = {}, x = {}):
	import ldap3
	cfg['module'] = "LDAP"
	table = util.guid("tmp_")
	if 'table' in x:
		table = x['table']
	try:
		util.debug(cfg, "Connecting to [" + x['server'] + ":" + str(x['port']) + "] and saving data to table [" + table + "]")
		s = ldap3.Server(x['server'], port = x['port']);
		if 'credential' in x: # Do a simple bind if a username and password were provided
			c = ldap3.Connection(s, auto_referrals = False, authentication = 'SIMPLE', user = cfg['creds'][x['credential']]['username'], password = cfg['creds'][x['credential']]['password']);
			c.open()
			c.bind()
		else:
			c = ldap3.Connection(s, auto_referrals = False);
			c.open()
		util.debug(cfg, str(c))
		attrs = []
		if 'attributes' in x: # Ask for every requested attribute
			for attr in x['attributes']:
				attrs.append(attr['attribute'])
		c.search(x['basedn'], x['filter'], ldap3.SEARCH_SCOPE_WHOLE_SUBTREE, attributes = attrs)
		tmp = "CREATE TABLE " + table + " (dn TEXT" # Create statement to be crafted
		qhs = "dn" # List of headers
		qms = "?" # Question marks for the insert statement
		for header in attrs: # Go through headers and craft create/insert statement
			tmp += ", " + header + " TEXT"
			qms += ", ?"
			qhs += ", " + header
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
		util.debug(cfg, "Column headers: " + qhs)
		rowcount = 0
		for row in c.response:
			rowcount += 1
			res = [row['dn']]
			for attr in attrs:
				if attr in row['attributes']:
					if type(row['attributes'][attr]) is list: # Check if returned attribute is a multi-attribute
						res.append(str(row['attributes'][attr][0]))
					else:
						res.append(str(row['attributes'][attr]))
				else: # The attribute does not exist, put an empty string
					res.append("")
			stmt = "INSERT INTO " + table + " (" + qhs + ") VALUES (" + qms + ")"
			if 'mode' in x:
				if x['mode'] == 'merge':
					stmt = "INSERT OR REPLACE INTO " + table + " (" + qhs + ") VALUES (" + qms + ")"
			cfg['db'].execute(stmt, res)
		cfg['db'].commit()
		util.info(cfg, "Read " + str(len(attrs)+1) + " columns, " + str(rowcount) + " rows.")
	except:
		util.err(cfg, str(sys.exc_info()[1]))
		return False
	return True
