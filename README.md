
# dbt-sqlite

A SQLite adapter plugin for dbt (data build tool)

## Notes

This is extremely 'alpha' quality software. Much is untested and things
are likely broken. Use at your own risk. Please report bugs!

- The 'database' value in configuration is irrelevant to SQLite and gets
stripped from the output of `ref()` and from SQL everywhere, and/or it
is always set to the value of 'database' in your target configuration.

- Schema are implemented as attached database files. SQLite automatically
assigns 'main' to the database file you initially connect to.

- Creating schemas is (not yet?) supported. There would need to be a way
to create paths for database files on the fly for the new schema that are
created. This impacts several features:

** [Custom schemas](https://docs.getdbt.com/docs/building-a-dbt-project/building-models/using-custom-schemas/) - 
dbt creates new "sub project" schemas for custom schemas, so this won't work.

** ephemeral materializations needs to create schemas, so this won't work.

- SQLite does not allow views in one schema (i.e. database file) to reference
objects in another schema. You'll get this error from SQLite: "view [someview]
cannot reference objects in database [somedatabase]". You must set
`materialized='table'` in models that reference other schemas.

- Some code is implemented as overrides in the `SQLiteAdapter` class rather
than tweaking the Jinja macros in `adapters.sql`, either because it was too
complicated or I couldn't figure out how to do it that way.

- This has been developed on Ubuntu 20.04, Python 3.8.5 (with sqlite 3.31.1),
dbt 0.18.1. It's largely untested elsewhere.

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

## Known Issues / TODOs

Need to implement:
- get_columns_in_relation

## Credits

Inspired by this initial work by stephen1000: https://github.com/stephen1000/dbt_sqlite

