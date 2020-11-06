
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
      # must be defined in schema_paths below. in most cases, this should be 'main'
      schema: 'main'
      # schemas and paths; at least one of these must be 'main'
      schema_paths: 'main=/home/jeff/etl.db;raw_data=/home/jeff/raw_data.db'
```

Set `profile: 'dbt_sqlite'` in your project's `dbt_project.yml` file.

## Notes

- There is no 'database' portion of relation names in SQLite so it gets
stripped from the output of `ref()` and from SQL everywhere. It still
needs to be set in the configuration and is used by dbt internally.

- Schema are implemented as attached database files. SQLite automatically
assigns 'main' to the database file you initially connect to.

- Creating schemas is (not yet?) supported. There would need to be a way
to create paths for database files on the fly for the new schema that are
created. This impacts several features:

  - [Custom schemas](https://docs.getdbt.com/docs/building-a-dbt-project/building-models/using-custom-schemas/) - 
dbt creates new "sub project" schemas for custom schemas, so this won't work.

  - ephemeral materializations needs to create schemas, so this won't work.

- SQLite does not allow views in one schema (i.e. database file) to reference
objects in another schema. You'll get this error from SQLite: "view [someview]
cannot reference objects in database [somedatabase]". You must set
`materialized='table'` in models that reference other schemas.

- Columns with numeric data in seed files won't load correctly unless you
explicitly specify 'int' datatype in the seeds configuration. You'll get an error
like "Error binding parameter N - probably unsupported type." (This doesn't
happen with postgres.)

- This has been developed on Ubuntu 20.04, Python 3.8.5 (with sqlite 3.31.1),
dbt 0.18.1. It's largely untested elsewhere.

## Development Notes / TODOs

Need to implement:
- get_columns_in_relation
- Is it possible to override BaseRelation.render() in leave off the database
part of the fully qualified relation name?

## Credits

Inspired by this initial work by stephen1000: https://github.com/stephen1000/dbt_sqlite

