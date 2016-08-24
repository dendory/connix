# Connix - Python cross-platform data manipulation utility

## About

Connix is a cross-platform data manipulation utility. It has three phases:

* input
* parse
* output

This utility can be used to import data from a large array of inputs, parse and interact with the data in a number of ways, then export the resulting data to a large number of outputs. All of the commands to tell Connix what to do are stored in a single JSON config file.

* Download:	[connix.zip](connix.zip)
* Source:	[https://github.com/dendory/connix](https://github.com/dendory/connix)

## Configuration

Connix reads from the config file you specify, or `sample.json` by default. The global configuration values are added to the top of the config file, and not for a specific module.

* `debug: [true|false]` Whether to display debugging messages or not.
* `log: <filename>` Where to write the log.
* `db: <filename>` The database file where to store data.
* `onerror: [continue|abort]` Defines how to handle module errors. Either **continue** with the processes or **abort** and quit.
* `credentials: [ { id: <unique id>, username: <username>, password: <password>, key: <access key>, keyfile: <filename> } ]` Sets credentials for use by modules.

## Modules

Modules handle **input**, **output**, **parse** or a combination of such.

### InitTable

This module will create, replace or remove tables for use with other modules.

#### input

* `id: <name>` This is a unique name for this input.
* `module: "inittable"` The module name to call.
* `table: <table name>` The name of the table to write data to. Optional, a random unique name will be used if not specified.
* `mode: [create|replace|remove]` The mode of operation. The module will **create** a table or abort, **replace** a table if it already exists or create it if not, or **remove** a table.
* `columns: [ { name: <name of the column>, primary: [true|false], type: [text|number] } ]` The columns definition for the table. Only one primary key must be specified. At least one column must exist, except for *remove*.

### CSV

The CSV module can read and write plain text CSV files. These files must have a header. Table columns are configured according to those column headers.

#### input

* `id: <name>` This is a unique name for this input.
* `module: "csv"` The module name to call.
* `file: <filename>` The CSV file to read.
* `table: <table name>` The name of the table where to store data. If it doesn't exist then it will be created on the fly. This parameter is optional, and a random unique name will be selected if not specified.
* `mode: [clear|add|merge]` The mode to use for data when added to an existing table. The module will either **clear** the existing data before insertion, **add** all data to the existing rows, or **merge** rows based on the table's primary key. You should pre-create the table with *inittable* and set a primary key to use *merge*.
* `delimiter: <character>` The character to use between columns. Optional, defaults to a comma.

#### output

* `id: <name>` This is a unique name for this output.
* `module: "csv"` The module name to call.
* `file: <filename>` The CSV file to write to. Optional, if unspecified a random unique file name is selected.
* `table: <table name>` The table containing the data to write.

### SQL

This module allows you to run SQL statements against your data.

#### parse

* `id: <name>` This is a unique name for this parse.
* `module: "sql"` The module name to call.
* `query: <sql statement>` A valid SQL statement to execute on the database.
* `type: [select|execute]` Whether the query should return data or not. Optional
* `table: <table name>` The name of the table to write data to, for select queries. Optional, a random unique name will be used if not specified.
* `mode: [clear|add|merge]` The mode to use for data when added to an existing table. The module will either **clear** the existing data before insertion, **add** all data to the existing rows, or **merge** rows based on the table's primary key. You should pre-create the table with *inittable* and set a primary key to use *merge*.

### ODBC

This module allows you to connect to a backend database using ODBC. Requires the pyodbc Python module to be installed.

#### input

* `id: <name>` This is a unique name for this input.
* `module: "odbc"` The module name to call.
* `dsn: <connection string>` A valid connection string to connect to a database server. Example: DRIVER={SQL Server};SERVER=10.0.0.1;DATABASE=test;UID=user;PWD=pass
* `query: <sql statement>` A valid SQL statement to query data over ODBC. Example: SELECT * FROM mytable
* `table: <table name>` The name of the table where to store data. If it doesn't exist then it will be created on the fly. This parameter is optional, and a random unique name will be selected if not specified.
* `mode: [clear|add|merge]` The mode to use for data when added to an existing table. The module will either **clear** the existing data before insertion, **add** all data to the existing rows, or **merge** rows based on the table's primary key. You should pre-create the table with *inittable* and set a primary key to use *merge*.

#### output

* `id: <name>` This is a unique name for this output.
* `module: "odbc"` The module name to call.
* `table: <table name>` The table containing the data to write.
* `dsn: <connection string>` A valid connection string to connect to a database server. Example: DRIVER={SQL Server};SERVER=10.0.0.1;DATABASE=test;UID=user;PWD=pass
* `odbctable: <table name>` The ODBC table name where to output data. Optional, a random unique name will be selected otherwise.
* `mode: [clear|add|merge]` The mode to use for data when added to an existing ODBC table. The module will either **clear** the existing data before insertion, **add** all data to the existing rows, or **merge** rows based on the table's primary key. You should pre-create the table with *inittable* and set a primary key to use *merge*.

### LDAP

This module allows you to create an LDAP query and get the resulting data. Requires the ldap3 Python module to be installed.

#### input

* `id: <name>` This is a unique name for this input.
* `module: "ldap"` The module name to call.
* `server: <LDAP server>` The LDAP server address.
* `port: <LDAP port>` The LDAP server port.
* `credential: <credential id>` Credentials to use for login (requires username/password, for Active Directory use DOMAIN\\userid). Optional.
* `basedn: <base dn>` The base dn to use for the query. Example: CN=Computers,DC=mydomain,DC=com
* `filter: <query filter>` The types of objects to return. Example: (&(objectCategory=computer))
* `index: <index attribute>` Unique attribute defining each entry. Optional, defaults to 'dn'.
* `attributes: [ { attribute: <attribute> } ]` Additional object attributes to retrieve. Note that multi-value attributes are not supported, only the first entry will be pulled in those cases.
* `table: <table name>` The name of the table where to store data. If it doesn't exist then it will be created on the fly. This parameter is optional, and a random unique name will be selected if not specified.
* `mode: [clear|add|merge]` The mode to use for data when added to an existing table. The module will either **clear** the existing data before insertion, **add** all data to the existing rows, or **merge** rows based on the table's primary key. You should pre-create the table with *inittable* and set a primary key to use *merge*.

### Screen

This is a simple module that can be used to display data directly to the standard output. 

#### output

* `id: <name>` This is a unique name for this output.
* `module: "screen"` The module name to call.
* `table: <table name>` The table containing the data to display.

### Files

This module lists files from a folder along with the file size, hash, the created and last modified date.

#### input

* `id: <name>` This is a unique name for this input.
* `module: "files"` The module name to call.
* `folder: <local path>` The folder to list from.
* `table: <table name>` The name of the table where to store data. If it doesn't exist then it will be created on the fly. This parameter is optional, and a random unique name will be selected if not specified.
* `mode: [clear|add|merge]` The mode to use for data when added to an existing table. The module will either **clear** the existing data before insertion, **add** all data to the existing rows, or **merge** rows based on the table's primary key. You should pre-create the table with *inittable* and set a primary key to use *merge*.

### HTML

This module will save a table in an HTML file, with optional header/footer. 

#### output

* `id: <name>` This is a unique name for this output.
* `module: "html"` The module name to call.
* `table: <table name>` The table containing the data to save.
* `file: <filename>` The HTML file to write to. Optional, if unspecified a random unique file name is selected.
* `headers: [true|false]` Add headers and CSS to make the table look prettier with built-in paging and search. Optional, if defaults to false.
* `htmlid: <id>` Value to use for the table ID tag. Must contain only letters and numbers, no space. Optional, defaults to a random unique value.

### Match

This module will copy rows from one table to another when the specified column matches (or doesn't match) a specific string or regular expression.

#### parse

* `id: <name>` This is a unique name for this parse.
* `module: "match"` The module name to call.
* `table: <table name>` The name of the table to read data from.
* `col: <column name>` The name of the column to match against.
* `match: <string>` The string that must be contained (or missing) from each row.
* `inverse: [true|false]` Whether the match string should be missing rather than present. Optional, defaults to false.
* `newtable: <table name>` The name of the table to write resulting rows to.
* `mode: [clear|add|merge]` The mode to use for data when added to an existing table. The module will either **clear** the existing data before insertion, **add** all data to the existing rows, or **merge** rows based on the table's primary key. You should pre-create the table with *inittable* and set a primary key to use *merge*.
