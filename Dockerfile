
ARG PYTHON_VERSION=3.9

FROM python:${PYTHON_VERSION}-buster

RUN apt-get update && apt-get -y install git python3 python3-pip python3-venv sqlite3 vim virtualenvwrapper wget

WORKDIR /opt/dbt-sqlite

RUN wget -q https://github.com/nalgeon/sqlean/releases/download/0.15.2/crypto.so
RUN wget -q https://github.com/nalgeon/sqlean/releases/download/0.15.2/text.so

RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install pytest pytest-dotenv dbt-core~=1.2.0rc1 dbt-tests-adapter==1.2.0rc1

WORKDIR /opt/dbt-sqlite/src 

COPY . .

RUN pip install -e .

ENV TESTDATA=/opt/dbt-sqlite/testdata

RUN mkdir $TESTDATA

VOLUME /opt/dbt-sqlite/testdata

WORKDIR /opt/dbt-sqlite/project

ENV HOME=/opt/dbt-sqlite/project

ENV PATH=$PATH:/opt/dbt-sqlite/src

VOLUME /opt/dbt-sqlite/project
