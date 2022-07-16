#!/bin/bash

docker build . -t dbt-sqlite

docker run \
     --rm \
     --name dbt-sqlite-test-container \
     dbt-sqlite ./run_tests.sh
