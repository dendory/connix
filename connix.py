#!/usr/bin/env python3
# Connix - (C) 2016 Patrick Lambert - Provided under the MIT license
# Main utility
from modules import util, config, csv, inittable
import sqlite3
import sys

# Default variables
version = "0.0.1"
cfg = {'module': "Main", 'debug': False, 'log': None, 'db': None}
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
	if rawcfg['json']['debug']:
		cfg['debug'] = True
	else:
		cfg['debug'] = False
	if 'log' in rawcfg['json']:
		 cfg['log'] = open(rawcfg['json']['log'], "a")
	cfg['db'] = sqlite3.connect(rawcfg['json']['db']) 
	input = rawcfg['json']['input']
	output = rawcfg['json']['output']
	parse = rawcfg['json']['parse']
except:
	util.err(cfg, "Invalid configuration for key " + str(sys.exc_info()[1]))
	util.exit(cfg, 1)

util.debug(cfg, "Input modules to process: " + str(len(input)))
util.debug(cfg, "Output modules to process: " + str(len(output)))
util.debug(cfg, "Number of parsing rules: " + str(len(parse)))

# Parse inputs
for x in input:
	util.info(cfg, "Parsing input [" + x['id'] + "] using module [" + x['module'] + "]")
	if x['module'].lower() == 'csv':
		csv.input(cfg, x)
	elif x['module'].lower() == 'inittable':
		inittable.input(cfg, x)
	else:
		util.err(cfg, "Unknown module name.")

# End
util.info(cfg, "Finished parsing. Total run time: " + str(util.unixtime() - perf) + "s")
util.exit(cfg, 0)
