#!/bin/bash

pip install -e .

# Leaving the database file between runs of pytest can mess up subsequent test runs.
# Since this runs in a fresh container each time, it's not an issue.

pytest test/sqlite.dbtspec

####

# dbt-sqlite overrides some stuff pertaining to 'docs generate'
# so exercise it using jaffle_shop repo

cd /tmp

git clone https://github.com/dbt-labs/jaffle_shop.git

cd /tmp/jaffle_shop

mkdir -p /root/.dbt

cat >> /root/.dbt/profiles.yml <<EOF

jaffle_shop:

  target: dev
  outputs:
    dev:
      type: sqlite
      threads: 1
      # database MUST exist in order for macros to work. its value is arbitrary.
      database: "database"
      schema: 'main'
      schemas_and_paths:
        main: '/tmp/jaffle_shop/jaffle_shop.db'
      schema_directory: '/tmp/jaffle_shop'
      extensions:
        - "/tmp/dbt-sqlite-tests/crypto.so"

EOF

dbt docs generate
