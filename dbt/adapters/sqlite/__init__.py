from dbt.adapters.sqlite.connections import SQLiteConnectionManager
from dbt.adapters.sqlite.connections import SQLiteCredentials
from dbt.adapters.sqlite.impl import SQLiteAdapter

from dbt.adapters.base import AdapterPlugin
from dbt.include import sqlite


Plugin = AdapterPlugin(
    adapter=SQLiteAdapter,
    credentials=SQLiteCredentials,
    include_path=sqlite.PACKAGE_PATH)
