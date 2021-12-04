#!/bin/bash

docker build . -t dbt-sqlite-test

docker run \
     --rm \
     --name dbt-sqlite-test-container \
     -v "$(pwd)":"/root/dbt-sqlite" \
     dbt-sqlite-test
