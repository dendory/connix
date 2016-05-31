#!/usr/bin/env python3
# Connix - (C) 2016 Patrick Lambert - Provided under the MIT license
# Main utility
from modules import util, config, csv, inittable, sql, odbc, ldap, screen, files
import sqlite3
import sys

# Default variables
version = "0.0.1"
cfg = {'module': "Main", 'debug': False, 'log': None, 'db': None, 'onerror': False}
input = {}
output = {}
parse = {}
perf = util.unixtime()

# Parse configuration
cfgfile = "connix.cfg"
if len(sys.argv) == 2:
	cfgfile = sys.argv[1]
util.info(cfg, "Connix v" + version + " starting. Reading configuration file [" + cfgfile + "]")
rawcfg = config.read_config(cfgfile)
if not rawcfg['status']:
	util.err(cfg, rawcfg['result'])
	util.exit(cfg, 1)
try:
	if 'debug' in rawcfg['json']:
		if rawcfg['json']['debug']:
			cfg['debug'] = True
		else:
			cfg['debug'] = False
	if 'log' in rawcfg['json']:
		 cfg['log'] = open(rawcfg['json']['log'], "a")
		 cfg['log'].write("===== " + util.datetime() + "\n")
	if 'onerror' in rawcfg['json']:
		if rawcfg['json']['onerror'] == 'abort':
			cfg['onerror'] = True
	cfg['db'] = sqlite3.connect(rawcfg['json']['db']) 
	input = rawcfg['json']['input']
	output = rawcfg['json']['output']
	parse = rawcfg['json']['parse']
except:
	util.err(cfg, "Invalid configuration for key " + str(sys.exc_info()[1]))
	util.exit(cfg, 1)

util.debug(cfg, "Connix v" + version + ", Python v" + sys.version + " " + sys.platform)
util.debug(cfg, "Input modules to process: " + str(len(input)))
util.debug(cfg, "Output modules to process: " + str(len(output)))
util.debug(cfg, "Number of parsing rules: " + str(len(parse)))

# Process inputs
for x in input:
	cfg['module'] = "Main"
	util.info(cfg, "Processing input [" + x['id'] + "] using module [" + x['module'] + "]")
	if x['module'].lower() == 'csv':
		if not csv.input(cfg, x) and cfg['onerror']:
			util.exit(cfg, 1)
	elif x['module'].lower() == 'odbc':
		if not odbc.input(cfg, x) and cfg['onerror']:
			util.exit(cfg, 1)
	elif x['module'].lower() == 'files':
		if not files.input(cfg, x) and cfg['onerror']:
			util.exit(cfg, 1)
	elif x['module'].lower() == 'ldap':
		if not ldap.input(cfg, x) and cfg['onerror']:
			util.exit(cfg, 1)
	elif x['module'].lower() == 'inittable':
		if not inittable.input(cfg, x) and cfg['onerror']:
			util.exit(cfg, 1)
	else:
		util.err(cfg, "Unknown module name.")

# Process parses
for x in parse:
	cfg['module'] = "Main"
	util.info(cfg, "Processing parse [" + x['id'] + "] using module [" + x['module'] + "]")
	if x['module'].lower() == 'sql':
		if not sql.parse(cfg, x) and cfg['onerror']:
			util.exit(cfg, 1)
	else:
		util.err(cfg, "Unknown module name.")

# Process outputs
for x in output:
	cfg['module'] = "Main"
	util.info(cfg, "Processing output [" + x['id'] + "] using module [" + x['module'] + "]")
	if x['module'].lower() == 'csv':
		if not csv.output(cfg, x) and cfg['onerror']:
			util.exit(cfg, 1)
	elif x['module'].lower() == 'odbc':
		if not odbc.output(cfg, x) and cfg['onerror']:
			util.exit(cfg, 1)
	elif x['module'].lower() == 'screen':
		if not screen.output(cfg, x) and cfg['onerror']:
			util.exit(cfg, 1)
	else:
		util.err(cfg, "Unknown module name.")

# End
cfg['module'] = "Main"
util.info(cfg, "Finished parsing. Total run time: " + str(util.unixtime() - perf) + "s")
util.exit(cfg, 0)
