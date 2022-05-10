
FROM ubuntu:20.04

RUN apt-get update && apt-get -y install git make python3 python3-pip python3-venv sqlite3 vim virtualenvwrapper wget

RUN mkdir /root/dbt-sqlite

WORKDIR /root/dbt-sqlite

RUN mkdir -p /tmp/dbt-sqlite-tests

RUN cd /tmp/dbt-sqlite-tests && wget https://github.com/nalgeon/sqlean/releases/download/0.12.2/crypto.so

RUN pip install dbt-core~=1.1.0

RUN pip install pytest pytest-dotenv dbt-tests-adapter==1.1.0

ENTRYPOINT ["./run_tests.sh"]
