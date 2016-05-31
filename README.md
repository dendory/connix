# Connix

Connix is a cross-platform data manipulation utility. It has three phases:

* input
* parse
* output

This utility can be used to import data from a large array of inputs, parse and interact with the data in a number of ways, then export the resulting data to a large number of outputs. All of the commands to tell Connix what to do are stored in a single JSON config file.

The current version is: **0.0.1**

## Installation

Install Python 3.x, then download and extract the Connix ZIP file. To run, type `python connix.py`. It should work fine on Linux and Windows.

## Configuration

Connix reads from the config file you specify, or `connix.cfg` by default. The global configuration values are added to the top of the config file, and not for a specific module.

* `debug: [true|false]` Whether to display debugging messages or not.
* `log: <filename>` Where to write the log.
* `db: <filename>` The database file where to store data.
* `onerror: [continue|abort]` Defines how to handle module errors. Either **continue** with the processes or **abort** and quit.

## Modules

Modules handle **input**, **output**, **parse** or a combination of such.

### CSV

The CSV module can read and write plain text CSV files. These files must have a header. Table columns are configured according to those column headers.

#### input

* `id: <name>` This is a unique name for the input.
* `module: "csv"` The module name to call.
* `file: <filename>` The CSV file to read.
* `table: <table name>` The name of the table where to store data. If it doesn't exist then it will be created on the fly. This parameter is optional, and a random unique name will be selected if not specified.
* `mode: [clear|add|merge]` The mode to use for data when added to an existing table. The module will either **clear** the existing data before insertion, **add** all data to the existing ones, or **merge** rows based on the table's primary key. You should pre-create the table with *inittable* and set a primary key to use *merge*.
* `delimiter: <character>` The character to use between columns. Optional, defaults to a comma.

#### output

* `id: <name>` This is a unique name for the output.
* `module: "csv"` The module name to call.
* `file: <filename>` The CSV file to write to. Optional, if unspecified a random unique file name is selected.
* `table: <table name>` The table containing the data to write.

### InitTable

This module will create, replace or remove tables for use with other modules.

#### input

* `id: <name>` This is a unique name for the input.
* `module: "inittable"` The module name to call.
* `table: <table name>` The name of the table to write data to. Optional, a random unique name will be used if not specified.
* `mode: [create|replace|remove]` The mode of operation. The module will **create** a table or abort, **replace** a table if it already exists or create it if not, or **remove** a table.
* `columns: [ { name: <name of the column>, primary: [true|false], type: [text|number] } ]` The columns definition for the table. Only one primary key must be specified. At least one column must exist.

### SQL

This module allows you to run SQL statements against your data.

#### parse

* `id: <name>` This is a unique name for the input.
* `module: "sql"` The module name to call.
* `query: <sql statement>` A valid SQL statement to execute on the database.

### ODBC

This module allows you to connect to a backend database using ODBC. Requires the pyodbc Python module to be installed.

#### input

* `id: <name>` This is a unique name for the input.
* `module: "odbc"` The module name to call.
* `dsn: <connection string>` A valid connection string to connect to a database server. Example: DRIVER={SQL Server};SERVER=10.0.0.1;DATABASE=test;UID=user;PWD=pass
* `query: <sql statement>` A valid SQL statement to query data over ODBC. Example: SELECT * FROM mytable
* `table: <table name>` The name of the table where to store data. If it doesn't exist then it will be created on the fly. This parameter is optional, and a random unique name will be selected if not specified.
* `mode: [clear|add|merge]` The mode to use for data when added to an existing table. The module will either **clear** the existing data before insertion, **add** all data to the existing ones, or **merge** rows based on the table's primary key. You should pre-create the table with *inittable* and set a primary key to use *merge*.

#### output

* `id: <name>` This is a unique name for the input.
* `module: "odbc"` The module name to call.
* `table: <table name>` The table containing the data to write.
* `dsn: <connection string>` A valid connection string to connect to a database server. Example: DRIVER={SQL Server};SERVER=10.0.0.1;DATABASE=test;UID=user;PWD=pass
* `odbctable: <table name>` The ODBC table name where to output data. Optional, a random unique name will be selected otherwise.
* `mode: [clear|add|merge]` The mode to use for data when added to an existing ODBC table. The module will either **clear** the existing data before insertion, **add** all data to the existing ones, or **merge** rows based on the table's primary key. You should pre-create the table with *inittable* and set a primary key to use *merge*.

### LDAP

This module allows you to create an LDAP query and get the resulting data. Requires the ldap3 Python module to be installed.

#### input

* `id: <name>` This is a unique name for the input.
* `module: "ldap"` The module name to call.
* `server: <LDAP server>` The LDAP server address.
* `port: <LDAP port>` The LDAP server port.
* `username: <username>` A valid user to bind to (for Active Directory it should be DOMAIN\\userid). Optional.
* `password: <password>` The password for that user. Optional.
* `basedn: <base dn>` The base dn to use for the query. Example: CN=Computers,DC=mydomain,DC=com
* `filter: <query filter>` The types of objects to return. Example: (&(objectCategory=computer))
* `attributes: [ { attribute: <attribute> } ]` Object attributes to retrieve. Note that multi-value attributes are not supported, only the first entry will be pulled in those cases.
* `table: <table name>` The name of the table where to store data. If it doesn't exist then it will be created on the fly. This parameter is optional, and a random unique name will be selected if not specified.
* `mode: [clear|add|merge]` The mode to use for data when added to an existing table. The module will either **clear** the existing data before insertion, **add** all data to the existing ones, or **merge** rows based on the table's primary key. You should pre-create the table with *inittable* and set a primary key to use *merge*.

### Screen

This is a simple module that can be used to display data directly to the standard output. 

#### output

* `id: <name>` This is a unique name for the input.
* `module: "odbc"` The module name to call.
* `table: <table name>` The table containing the data to display.

### Files

This module lists files from a folder.

#### input

* `id: <name>` This is a unique name for the input.
* `module: "files"` The module name to call.
* `folder: <local path>` The folder to list from.
* `table: <table name>` The name of the table where to store data. If it doesn't exist then it will be created on the fly. This parameter is optional, and a random unique name will be selected if not specified.
* `mode: [clear|add|merge]` The mode to use for data when added to an existing table. The module will either **clear** the existing data before insertion, **add** all data to the existing ones, or **merge** rows based on the table's primary key. You should pre-create the table with *inittable* and set a primary key to use *merge*.
