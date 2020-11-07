
# dbt-sqlite

A SQLite adapter plugin for dbt (data build tool)

This is an 'experimental' plugin. Features are missing, need to be
implemented, or broken. Use at your own risk. Issues and PRs welcome!

## How to Use This

Install this package.

Create an entry in your `~/.dbt/profiles.yml` file with the following configuration:

```
dbt_sqlite:

  target: dev
  outputs:
    dev:
      type: sqlite
      threads: 1
      # value of 'database' is arbitrary
      database: "database"
      # value of 'schema' must be defined in schema_paths below. in most cases, this should be 'main'
      schema: 'main'
      # connect schemas to paths: at least one of these must be 'main'
      schemas_and_paths: 'main=/my_project/data/etl.db;dataset=/my_project/data/dataset_v1.db'
      # directory where new schemas are created by dbt as new database files
      schema_directory: '/myproject/data/schemas'
```

Set `profile: 'dbt_sqlite'` in your project's `dbt_project.yml` file.

## Notes

- There is no 'database' portion of relation names in SQLite so it gets
stripped from the output of `ref()` and from SQL everywhere. It still
needs to be set in the configuration and is used by dbt internally.

- Schema are implemented as attached database files. SQLite automatically
assigns 'main' to the database file you initially connect to. (TODO: add warning
about references and renaming schemas/database files, and what creating/schemas
does)

- SQLite does not allow views in one schema (i.e. database file) to reference
objects in another schema. You'll get this error from SQLite: "view [someview]
cannot reference objects in database [somedatabase]". You must set
`materialized='table'` in models that reference other schemas.

- Materializations are simplified: they drop and re-create the model, instead of
doing the backup-and-swap-in new mode that the other dbt database adapters
support. This choice was made because SQLite doesn't support `DROP ... CASCADE`
or `ALTER VIEW` or provide information about relation dependencies in a
information_schema-like relation. Taken together, these limitations make it really
difficult to make the backup-and-swap-in functionality work properly.

- Columns with numeric data in seed files won't load correctly unless you
explicitly specify 'int' datatype in the seeds configuration. You'll get an error
like "Error binding parameter N - probably unsupported type." (This doesn't
happen with postgres.)

- This has been developed on Ubuntu 20.04, Python 3.8.5 (with sqlite 3.31.1),
dbt 0.18.1. It's largely untested elsewhere.

## Development Notes / TODOs

- Is it possible to override BaseRelation.render() in leave off the database
part of the fully qualified relation name?

- snapshots don't work yet

- incremental materializations don't work yet

- adapter tests don't specify column types when loading seeds, and this raises
an error. agate infers the types, and sqlite doesn't like what gets passed into
query bindings for insert.

## Running Tests

Install the `pytest-dbt-adapter` package and run the test specs in this repository:

```
pip install pytest-dbt-adapter

# these paths need to exist for tests to write data
mkdir -p /tmp/dbt-sqlite-tests
mkdir -p /tmp/dbt-sqlite-tests/schemas

pytest test/sqlite.dbtspec
```

## Credits

Inspired by this initial work by stephen1000: https://github.com/stephen1000/dbt_sqlite

