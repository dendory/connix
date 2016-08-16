#!/usr/bin/env python3
# Connix - (C) 2016 Patrick Lambert - Provided under the MIT license
# Main utility
from modules import util, config, csv, inittable, sql, odbc, ldap, screen, files
import sqlite3
import sys

# Default variables
version = "0.0.3"
cfg = {'module': "Main", 'debug': False, 'log': None, 'db': None, 'onerror': False, 'creds': {}}
input = {}
output = {}
parse = {}
perf = util.unixtime()

# Parse configuration
cfgfile = "sample.json" # Default config file
if len(sys.argv) == 2:
	cfgfile = sys.argv[1] # Take config file from command line arguments
util.info(cfg, "Connix v" + version + " starting. Reading configuration file [" + cfgfile + "]")
rawcfg = config.read_config(cfgfile) # Read config
if not rawcfg['status']:
	util.err(cfg, rawcfg['result']) # Config file does not exist or is corrupted
	util.exit(cfg, 1)
try:
	if 'debug' in rawcfg['json']:
		if rawcfg['json']['debug']: # Debug mode
			cfg['debug'] = True
		else:
			cfg['debug'] = False
	if 'credentials' in rawcfg['json']:
		for cred in rawcfg['json']['credentials']: # Iterate over all credentials
			cfg['creds'][cred['id']] = cred
	if 'log' in rawcfg['json']: # Set logging file and start logging
		 cfg['log'] = open(rawcfg['json']['log'], "a")
		 cfg['log'].write("===== " + util.datetime() + "\n")
	if 'onerror' in rawcfg['json']: # Set whether to abort if we run into an error
		if rawcfg['json']['onerror'] == 'abort':
			cfg['onerror'] = True
	cfg['db'] = sqlite3.connect(rawcfg['json']['db']) # Open DB file
	input = rawcfg['json']['input'] # Set inputs
	output = rawcfg['json']['output'] # Set outputs
	parse = rawcfg['json']['parse'] # Set parses
except:
	util.err(cfg, "Invalid configuration for key " + str(sys.exc_info()[1]))
	util.exit(cfg, 1)

util.debug(cfg, "Connix v" + version + ", Python v" + sys.version + " " + sys.platform)
util.debug(cfg, "Input modules to process: " + str(len(input)))
util.debug(cfg, "Output modules to process: " + str(len(output)))
util.debug(cfg, "Number of parsing rules: " + str(len(parse)))

# Process inputs
for x in input:
	cfg['module'] = "Main" # Reset module to main, each module is responsible for setting their own module name
	util.info(cfg, "Processing input [" + x['id'] + "] using module [" + x['module'] + "]")
	if x['module'].lower() == 'csv': # Get data from a CSV file
		if not csv.input(cfg, x) and cfg['onerror']:
			util.exit(cfg, 1)
	elif x['module'].lower() == 'odbc': # Get data from an ODBC database
		if not odbc.input(cfg, x) and cfg['onerror']:
			util.exit(cfg, 1)
	elif x['module'].lower() == 'files': # Get data from files
		if not files.input(cfg, x) and cfg['onerror']:
			util.exit(cfg, 1)
	elif x['module'].lower() == 'ldap': # Connect to LDAP (or Active Directory) server and get data
		if not ldap.input(cfg, x) and cfg['onerror']:
			util.exit(cfg, 1)
	elif x['module'].lower() == 'inittable': # Create, remove or replace a table in preparation for data insertion
		if not inittable.input(cfg, x) and cfg['onerror']:
			util.exit(cfg, 1)
	else:
		util.err(cfg, "Unknown module name.")

# Process parses
for x in parse:
	cfg['module'] = "Main" # Reset module to main, each module is responsible for setting their own module name
	util.info(cfg, "Processing parse [" + x['id'] + "] using module [" + x['module'] + "]")
	if x['module'].lower() == 'sql': # Run arbitrary SQL query on the database
		if not sql.parse(cfg, x) and cfg['onerror']:
			util.exit(cfg, 1)
	else:
		util.err(cfg, "Unknown module name.")

# Process outputs
for x in output:
	cfg['module'] = "Main" # Reset module to main, each module is responsible for setting their own module name
	util.info(cfg, "Processing output [" + x['id'] + "] using module [" + x['module'] + "]")
	if x['module'].lower() == 'csv': # Write contents of a table in a CSV file
		if not csv.output(cfg, x) and cfg['onerror']:
			util.exit(cfg, 1)
	elif x['module'].lower() == 'odbc': # Send contents of a table to an ODBC database
		if not odbc.output(cfg, x) and cfg['onerror']:
			util.exit(cfg, 1)
	elif x['module'].lower() == 'screen': # Show contents of a table on the screen
		if not screen.output(cfg, x) and cfg['onerror']:
			util.exit(cfg, 1)
	else:
		util.err(cfg, "Unknown module name.")

# End
cfg['module'] = "Main" # Reset module to main and exit
util.info(cfg, "Finished parsing. Total run time: " + str(util.unixtime() - perf) + "s")
util.exit(cfg, 0)
