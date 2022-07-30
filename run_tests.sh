#!/bin/bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

# Leaving the database file between runs of pytest can mess up subsequent test runs.
# Since this runs in a fresh container each time, it's not an issue.

pytest tests/functional

####

# dbt-sqlite overrides some stuff pertaining to 'docs generate'
# so exercise it using jaffle_shop repo

# dbt-sqlite overrides some stuff pertaining to 'docs generate'
# so exercise it using jaffle_shop repo

cd $HOME

git clone --depth 1 https://github.com/dbt-labs/jaffle_shop.git

cd jaffle_shop

git pull

mkdir -p /tmp/jaffle_shop

mkdir -p $HOME/.dbt

if [ -f $HOME/.dbt/profiles.yml ]; then
    echo "ERROR: profiles.yml already exists, refusing to overwrite it"
    exit 1
fi

cat >> $HOME/.dbt/profiles.yml <<EOF

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
        - "/tmp/dbt-sqlite-tests/math.so"
        - "/tmp/dbt-sqlite-tests/text.so"

EOF

dbt docs generate
