# Connix - (C) 2016 Patrick Lambert - Provided under the MIT license
# CSV module - This will read a CSV file containing headers, create a staging table for the data based on the
# columns/rows in the CSV, then merge that data into an existing table 
from modules import util
import csv
import sys
import os

# Process input
def input(cfg = {}, x = {}):
	cfg['module'] = "CSV"
	table = util.guid("tmp_")
	if 'table' in x:
		table = x['table']
	try:
		util.debug(cfg, "Reading file [" + x['file'] + "] and sending data to table [" + table + "]")
		f = open(x['file'], "r") # Read CSV file
		delim = ","
		if 'delimiter' in x:
			delim = x['delimiter']
		csvreader = csv.reader(f, delimiter=delim)
		headers = next(csvreader)
		util.debug(cfg, "Headers found: " + str(headers))
		tmp = "CREATE TABLE " + table + " (" # Create statement to be crafted
		qhs = "" # List of headers
		qms = "" # Question marks for the insert statement
		found = False
		colcount = 0
		for header in headers: # Go through headers and craft create/insert statement
			if found:
				tmp += ", "
				qms += ", "
				qhs += ", "
			found = True
			tmp += header + " TEXT"
			qms += "?"
			qhs += header
			colcount += 1
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
		rowcount = 0
		for line in csvreader: # Go through each line of the CSV and insert values
			stmt = "INSERT INTO " + table + " (" + qhs + ") VALUES (" + qms + ")"
			if 'mode' in x:
				if x['mode'] == 'merge':
					stmt = "INSERT OR REPLACE INTO " + table + " (" + qhs + ") VALUES (" + qms + ")"
			cfg['db'].execute(stmt, line)
			rowcount += 1
		cfg['db'].commit()
		util.info(cfg, "Read " + str(colcount) + " columns, " + str(rowcount) + " rows.") 
		f.close()
	except:
		util.err(cfg, str(sys.exc_info()[1]))
		return False
	cfg['module'] = "Main"
	return True

# Process output
def output(cfg = {}, x = {}):
	cfg['module'] = "CSV"
	filename = util.guid("tmp_")
	if 'file' in x:
		filename = x['file']
	try:
		util.debug(cfg, "Writing table [" + x['table'] + "] to file [" + filename + "]")
		f = open(filename, "w", newline='')
		sql = cfg['db'].cursor()
		sql.execute("SELECT * FROM " + x['table'])
		csvwriter = csv.writer(f)
		csvwriter.writerow([i[0] for i in sql.description]) # Write headers
		csvwriter.writerows(sql) # Write rows
		f.close()
		util.info(cfg, "Wrote " + str(os.path.getsize(filename)) + " bytes.")
	except:
		util.err(cfg, str(sys.exc_info()[1]))
		return False
	return True
