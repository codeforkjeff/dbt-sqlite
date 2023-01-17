
ARG PYTHON_VERSION=3.9

FROM python:${PYTHON_VERSION}-bullseye

RUN apt-get update && apt-get -y install git python3 python3-pip python3-venv sqlite3 vim virtualenvwrapper wget

WORKDIR /opt/dbt-sqlite

RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install pytest pytest-dotenv dbt-core~=1.2.0 dbt-tests-adapter~=1.2.0

RUN wget -q https://github.com/nalgeon/sqlean/releases/download/0.15.2/crypto.so
RUN wget -q https://github.com/nalgeon/sqlean/releases/download/0.15.2/math.so
RUN wget -q https://github.com/nalgeon/sqlean/releases/download/0.15.2/text.so

WORKDIR /opt/dbt-sqlite/src 

COPY setup.py .
COPY dbt ./dbt

RUN pip install .

COPY run_tests.sh .
COPY pytest.ini .
COPY tests ./tests

ENV TESTDATA=/opt/dbt-sqlite/testdata

RUN mkdir $TESTDATA

VOLUME /opt/dbt-sqlite/testdata

WORKDIR /opt/dbt-sqlite/project

ENV PATH=$PATH:/opt/dbt-sqlite/src

VOLUME /opt/dbt-sqlite/project
