
FROM ubuntu:20.04

RUN apt-get update && apt-get -y install git make python3 python3-pip python3-venv sqlite3 vim virtualenvwrapper wget

RUN mkdir /root/dbt-sqlite

WORKDIR /root/dbt-sqlite

COPY bootstrap_test_env.sh .

RUN ./bootstrap_test_env.sh

COPY . .

RUN pip install -e .

ENTRYPOINT ["/bin/bash"]
