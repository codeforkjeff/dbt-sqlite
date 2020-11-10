
# dbt-sqlite

A [SQLite](https://sqlite.org) adapter plugin for dbt (data build tool)

This is an experimental plugin. Please read these docs carefully and
use at your own risk. Issues and PRs welcome!

## How to Use This

Install this package: `pip install dbt-sqlite`

Create an entry in your `~/.dbt/profiles.yml` file with the following configuration:

```YAML
dbt_sqlite:

  target: dev
  outputs:
    dev:
      type: sqlite

      # sqlite locks the whole db on writes so anything > 1 won't help
      threads: 1

      # value is arbitrary
      database: "database"

      # value of 'schema' must be defined in schema_paths below. in most cases,
      # this should be 'main'
      schema: 'main'

      # connect schemas to paths: at least one of these must be 'main'
      schemas_and_paths: 'main=/my_project/data/etl.db;dataset=/my_project/data/dataset_v1.db'

      # directory where all *.db files are attached as schema
      schema_directory: '/myproject/data/schemas'

      # optional: semi-colon separated list of file paths for SQLite extensions to load.
      # digest.so is needed to provide for snapshots to work; see README
      extensions: "/path/to/sqlite-digest/digest.so"

```

Set `profile: 'dbt_sqlite'` in your project's `dbt_project.yml` file.

## Notes

- There is no 'database' portion of relation names in SQLite so it gets
stripped from the output of `ref()` and from SQL everywhere. It still
needs to be set in the configuration and is used by dbt internally.

- Schema are implemented as attached database files. (SQLite conflates databases
and schemas.)

  - SQLite automatically assigns 'main' to the file you initially connect to,
  so this must be defined in your profile. Other schemas defined in your profile
  get attached when database connection is created.

  - If dbt needs to create a new schema, it will be created in `schema_directory`
  as `schema_name.db`. Dropping a schema results in dropping all its relations
  and detaching the database file from the session.

  - Schema names are stored in view definitions, so when you access a non-'main'
  database file outside dbt, you'll need to attach it using the same name, or
  the views won't work.

  - SQLite does not allow views in one schema (i.e. database file) to reference
  objects in another schema. You'll get this error from SQLite: "view [someview]
  cannot reference objects in database [somedatabase]". You must set
  `materialized='table'` in models that reference other schemas.

- Materializations are simplified: they drop and re-create the model, instead of
doing the backup-and-swap-in new mode that the other dbt database adapters
support. This choice was made because SQLite doesn't support `DROP ... CASCADE`
or `ALTER VIEW` or provide information about relation dependencies in something
information_schema-like. These limitations make it really difficult to make the
backup-and-swap-in functionality work properly. Given how SQLite aggressively
[locks](https://sqlite.org/lockingv3.html) the database anyway, it's probably
not worth the effort.

- This has been developed on Ubuntu 20.04, Python 3.8.5 (with sqlite 3.31.1),
dbt 0.18.1. It's largely untested elsewhere.

## Building the digest extension for SQLite

For snapshots to work, you need to build the `digest` extension to get an `md5()`
function. On Ubuntu, run:

```
git clone https://github.com/mpdn/sqlite-digest

cd sqlite-digest

sudo apt install gcc libssl-dev libsqlite3-dev

make
```

This will create `digest.so`. Point to it in your profile config as shown in the
example above.

## Development Notes / TODOs

...

## Running Tests

Install the `pytest-dbt-adapter` package and run the test specs in this repository:

```
pip install pytest-dbt-adapter

# these paths need to exist for tests to write data
mkdir -p /tmp/dbt-sqlite-tests
mkdir -p /tmp/dbt-sqlite-tests/schemas

pytest test/sqlite.dbtspec
```

Remember to delete the database file referenced in `test/sqlite.dbtspec`
between runs of pytest, otherwise leftover state from failures can mess up subsequent test runs.

## Credits

Inspired by this initial work by stephen1000: https://github.com/stephen1000/dbt_sqlite

https://github.com/jwills/dbt-duckdb/ - useful for ideas on working with
another embedded database

https://github.com/fishtown-analytics/dbt-spark/ - spark also has two-part
relation names (no 'database')
