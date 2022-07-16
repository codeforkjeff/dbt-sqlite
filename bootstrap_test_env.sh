#!/bin/sh
# bootstrap test environment

python3 -m pip install --upgrade pip

pip install dbt-core~=1.2.0rc1
pip install pytest pytest-dotenv dbt-tests-adapter==1.2.0rc1

mkdir -p /tmp/dbt-sqlite-tests
cd /tmp/dbt-sqlite-tests
wget https://github.com/nalgeon/sqlean/releases/download/0.12.2/crypto.so
