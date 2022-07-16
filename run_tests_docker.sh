#!/bin/bash

docker build . -t dbt-sqlite

docker run \
     --rm \
     --name dbt-sqlite-test-container \
     -v "$(pwd)":"/root/dbt-sqlite" \
     dbt-sqlite ./run_tests.sh
