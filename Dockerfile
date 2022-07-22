
FROM ubuntu:20.04

RUN apt-get update && apt-get -y install git python3 python3-pip python3-venv sqlite3 vim virtualenvwrapper wget

WORKDIR /opt/dbt-sqlite

RUN wget -q https://github.com/nalgeon/sqlean/releases/download/0.15.2/crypto.so
RUN wget -q https://github.com/nalgeon/sqlean/releases/download/0.15.2/text.so

# RUN useradd --home-dir /opt/dbt-sqlite/project dbtsqlite
# RUN mkdir /opt/dbt-sqlite/project
# RUN chown dbtsqlite.dbtsqlite -R /opt/dbt-sqlite

# USER dbtsqlite

# RUN cd /opt/dbt-sqlite && python3 -m venv dbt_env

# RUN . /opt/dbt-sqlite/dbt_env/bin/activate \
#     && python3 -m pip install --upgrade pip \
#     && pip install pytest pytest-dotenv dbt-core~=1.2.0rc1 dbt-tests-adapter==1.2.0rc1

RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install pytest pytest-dotenv dbt-core~=1.2.0rc1 dbt-tests-adapter==1.2.0rc1

WORKDIR /opt/dbt-sqlite/src 

COPY . .
# USER root
# RUN chown dbtsqlite.dbtsqlite -R /opt/dbt-sqlite/project/src
# USER dbtsqlite

# RUN . /opt/dbt-sqlite/dbt_env/bin/activate && pip install -e .
RUN pip install -e .

WORKDIR /opt/dbt-sqlite/project

ENV HOME=/opt/dbt-sqlite/project

ENV PATH=$PATH:/opt/dbt-sqlite/src

VOLUME /opt/dbt-sqlite/project

# ENTRYPOINT ["/bin/bash", "-c"]
