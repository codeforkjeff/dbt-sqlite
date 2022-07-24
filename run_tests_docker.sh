#!/bin/bash

docker build . -t dbt-sqlite

docker rm dbt-sqlite-test-container

docker run \
     --name dbt-sqlite-test-container \
     dbt-sqlite run_tests.sh
