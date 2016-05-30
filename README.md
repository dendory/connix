# Connix

Python data manipulation utility.

These are the module names and configuration parameters expected:

## Config

The global configuration values are added to the top of the config file, and not for a specific module.

* debug: [true|false] - Whether to display debugging messages or not.
* log: <filename> - Where to write the log.
* db: <filename> - The database file where to store data.

## Modules

Modules handle **input**, **output**, **process** or a combination of such.

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

#### process

### InitTable

This module will create, replace or remove tables for use with other modules.

#### input

* `id: <name>` This is a unique name for the input.
* `module: "inittable"` The module name to call.
* `table: <table name>` The name of the table. Optional, a random unique name will be used if not specified.
* `mode: [create|replace|remove]` The mode of operation. The module will **create** a table or abort, **replace** a table if it already exists or create it if not, or **remove** a table.
* `columns: { name: <name of the column>, primary: [true|false], type: [text|number] }` The columns definition for the table. Only one primary key must be specified. At least one column must exist.

