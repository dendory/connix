# Connix - (C) 2016 Patrick Lambert - Provided under the MIT license
# HTML module - output a specific table as an HTML table in a file
from modules import util
import sys

# Process output
def output(cfg = {}, x = {}):
	cfg['module'] = "HTML"
	try:
		numrow = 0
		filename = util.guid("tmp_") + ".html" # File name to write HTML to
		if 'file' in x:
			filename = x['file']
		htmlid = util.guid() # ID for the table
		if 'htmlid' in x:
			htmlid = x['htmlid']
		util.debug(cfg, "Saving table [" + x['table'] + "] to HTML file [" + filename + "]")
		sql = cfg['db'].cursor()
		sql.execute("SELECT * FROM " + x['table'])
		f = open(filename, "w", newline='')
		if 'headers' in x and x['headers']: # Craft headers using Datatables, JQuery and Bootstrap
			f.write("<HTML><HEAD>\n")
			f.write("<LINK REL='stylesheet' TYPE='text/css' HREF='//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'/>\n")
			f.write("<LINK REL='stylesheet' TYPE='text/css' HREF='//cdn.datatables.net/1.10.12/css/jquery.dataTables.min.css'/>\n")
			f.write("<SCRIPT TYPE='text/javascript' SRC='//code.jquery.com/jquery-1.11.3.js'></SCRIPT>\n")
			f.write("<SCRIPT TYPE='text/javascript' SRC='//cdn.datatables.net/1.10.12/js/jquery.dataTables.js'></SCRIPT>\n")
			f.write("<META CHARSET='utf-8'>\n")
			f.write("<META HTTP-EQUIV='X-UA-Compatible' CONTEN='IE=edge'>\n")
			f.write("<META NAME='viewport' CONTENT='width=device-width, initial-scale=1'>\n")
			f.write("</HEAD><BODY>\n")
			f.write("<DIV CLASS='container'>\n")
			f.write("<DIV CLASS='page-header'><H1>" + x['table'] + "</H1></DIV>\n")
		f.write("<TABLE ID='" + htmlid + "' CLASS='table'><THEAD>\n<TR>")
		for r in sql.description: # Write HTML table headers based on SQL table headers
			f.write("<TH>" + str(r[0]) + "</TH>")
		f.write("</TR>\n</THEAD><TBODY>\n")
		for row in sql.fetchall(): # Iterate over rows
			numrow += 1
			f.write("<TR>")
			for r in row: # Write each cell
				f.write("<TD>" + str(r) + "</TD>")
			f.write("</TR>\n")
		f.write("</TBODY></TABLE>\n")
		if 'headers' in x and x['headers']: # Write bottom of the page
			f.write("<SCRIPT TYPE='text/javascript'>$(document).ready(function() { $('#" + htmlid + "').DataTable(); } );</SCRIPT>\n")
			f.write("</DIV>\n")
			f.write("</BODY></HTML>\n")		
		f.close()
		util.info(cfg, "Wrote " + str(numrow) + " rows.")
	except:
		util.err(cfg, str(sys.exc_info()[1]))
		return False
	return True
