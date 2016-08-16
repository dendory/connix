# Connix - (C) 2016 Patrick Lambert - Provided under the MIT license
# Configuration parsing
import sys
import time
import random
import string

# Print an error and quit
def err(cfg, msg):
	print("* Error: " + msg)
	if cfg['log']:
		cfg['log'].write("ERROR " + str(unixtime()) + " " + cfg['module'] + " - " + msg + "\n")

# Print a message to the screen
def info(cfg, msg):
	print("* " + msg)
	if cfg['log']:
		cfg['log'].write("INFO  " + str(unixtime()) + " " + cfg['module'] + " - " + msg + "\n")

# Print a message to the screen
def debug(cfg, msg):
	if cfg['debug']:
		print("* Debug: " + msg)
		if cfg['log']:
			cfg['log'].write("DEBUG " + str(unixtime()) + " " + cfg['module'] + " - " + msg + "\n")

# Clean up and exit
def exit(cfg, status):
	if cfg['debug']:
		debug(cfg, "Exiting")
	if cfg['log']:
		cfg['log'].close()
	if cfg['db']:
		cfg['db'].close()
	quit(status)

# Get a unique ID based on current time
def guid(prefix = ""):
	return prefix + ''.join(random.choice(string.ascii_letters + string.digits) for i in range(12)) + str(hex(int(time.time())))

# Current unix time
def unixtime():
	return int(time.time())

# Current date and time
def datetime():
	return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

# Return the hash of a file
def hashfile(filename):
	import hashlib
	try:
		BLOCKSIZE = 65536
		hasher = hashlib.md5()
		with open(filename, "rb") as f:
			buf = f.read(BLOCKSIZE)
			while len(buf) > 0:
				hasher.update(buf)
				buf = f.read(BLOCKSIZE)
		return str(hasher.hexdigest())
	except:
		return ""
