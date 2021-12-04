
FROM ubuntu:20.04

RUN apt-get update && apt-get -y install git make python3 python3-pip python3-venv sqlite3 vim virtualenvwrapper wget

RUN mkdir /root/dbt-sqlite

WORKDIR /root/dbt-sqlite

RUN mkdir -p /tmp/dbt-sqlite-tests

RUN cd /tmp/dbt-sqlite-tests && wget https://github.com/nalgeon/sqlean/releases/download/0.12.2/crypto.so

RUN pip install dbt==0.21.1

# NOTE: dbt 0.19.x doesn't work with pytest-dbt-adapter >= 0.5.0; use 0.4.0
# see https://github.com/dbt-labs/dbt-adapter-tests/issues/20
#
# pytest-dbt-adapter 0.6.0 doesn't seem to work with dbt 0.21.1,
# I think it's intended for the forthcoming 1.0.0 dbt release?
RUN pip install pytest-dbt-adapter==0.5.1

ENTRYPOINT ["./run_tests.sh"]
