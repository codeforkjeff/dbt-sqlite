
# dbt-sqlite

A [SQLite](https://sqlite.org) adapter plugin for [dbt](https://www.getdbt.com/) (data build tool)

Please read these docs carefully and use at your own risk. Issues and PRs welcome!

## The Use Case

SQLite is an embedded SQL database. It comes included with most Python
distributions and requires no installation or configuration. It can be
a good choice if your project meets any of these criteria:

- you store the database file on fast, local storage
(not on a network drive)
- the amount of data is relatively small (GBs, not TBs)
- you're a data team of one with no need to share access to a database
- your end goal is to export the results of your pipeline(s) into other
systems for multi-user access or into BI/viz tools for analysis (i.e.
you're doing ETL vs ELT)
- your project is a proof of concept, to eventually be moved into
another database or data warehouse platform
- you want others to be able to deploy your data build without the
overhead/cost of a full RDBMS or signing up for a data warehouse platform

SQLite can be surprisingly fast, despite the query optimizer not being as
sophisticated as other databases and data warehouse platforms. Tip: materialize
your models as tables and create indexes in post-hooks to speed up filtering
and joins.

## How to Use This

Use the right version. Starting with the release of dbt-core 1.0.0,
versions of dbt-sqlite are aligned to the same major+minor
[version](https://semver.org/) of dbt-core.

- versions 1.1.x of this adapter work with dbt-core 1.1.x
- versions 1.0.x of this adapter work with dbt-core 1.0.x
- versions 0.2.x of this adapter work with dbt 0.20.x and 0.21.x
- versions 0.1.x of this adapter work with dbt 0.19.x
- versions 0.0.x of this adapter work with dbt 0.18.x

Install this package:

```
# run this to install the latest version
pip install dbt-sqlite

# OR run this to install a specific version
pip install dbt-sqlite==1.0.0
```

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
      schemas_and_paths:
        main: '/my_project/data/etl.db'
        dataset: '/my_project/data/dataset_v1.db'

      # directory where all *.db files are attached as schema, using base filename
      # as schema name, and where new schema are created. this can overlap with the dirs of
      # files in schemas_and_paths as long as there's no conflicts.
      schema_directory: '/my_project/data'

      # optional: list of file paths of SQLite extensions to load.
      # crypto.so is needed for snapshots to work; see README
      extensions:
        - "/path/to/sqlean/crypto.so"

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
doing the backup-and-swap-in new model that the other dbt database adapters
support. This choice was made because SQLite doesn't support `DROP ... CASCADE`
or `ALTER VIEW` or provide information about relation dependencies in something
information_schema-like. These limitations make it really difficult to make the
backup-and-swap-in functionality work properly. Given how SQLite aggressively
[locks](https://sqlite.org/lockingv3.html) the database anyway, it's probably
not worth the effort.

## SQLite Extensions

For snapshots to work, you'll need the `crypto` module from SQLean to get an `md5()`
function. It's recommended that you install all the SQLean modules, as they provide
many common SQL functions missing from SQLite.

Precompiled binaries are available for download from the [SQLean github repository page](https://github.com/nalgeon/sqlean).
You can also compile them yourself if you want.

Point to these module files in your profile config as shown in the example above.

Mac OS seems to ship with [SQLite libraries that do not have support for loading extensions compiled in](https://docs.python.org/3/library/sqlite3.html#f1),
so this won't work "out of the box." Accordingly, snapshots won't work.
If you need snapshot functionality, you'll need to compile SQLite/python
or find a python distribution for Mac OS with this support.

## Development Notes / TODOs

...

### Publishing a release to PyPI

Because I forget...

```
# assumes ~/.pypirc is already set up

workon dbt-sqlite-devel

vi dbt/adapters/sqlite/__version__.py # update version
vi setup.py # update dbt-core dependency if appropriate

# start clean
rm -rf dist/ build/ *.egg-info

# make sure tools are up to date
python -m pip install --upgrade setuptools wheel twine

# build
python setup.py sdist bdist_wheel

# upload to PyPI
python -m twine upload dist/*

git commit
git tag vXXX
git push --tags

# go to github and "Draft a new release"
```

## Running Tests

```
./run_tests_docker.sh
```

## Credits

Inspired by this initial work by stephen1000: https://github.com/stephen1000/dbt_sqlite

https://github.com/jwills/dbt-duckdb/ - useful for ideas on working with
another embedded database

https://github.com/fishtown-analytics/dbt-spark/ - spark also has two-part
relation names (no 'database')
