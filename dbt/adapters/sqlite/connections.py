
from contextlib import contextmanager
from dataclasses import dataclass, field
import glob
import os.path
import sqlite3
from typing import Optional, Tuple, Any, Dict, List


from dbt.adapters.base import Credentials
from dbt.adapters.sql import SQLConnectionManager
from dbt.contracts.connection import AdapterResponse
from dbt.contracts.connection import Connection
from dbt.exceptions import (
    DatabaseException,
    FailedToConnectException,
    RuntimeException
)
from dbt.logger import GLOBAL_LOGGER as logger


@dataclass
class SQLiteCredentials(Credentials):
    """ Required connections for a SQLite connection"""

    schemas_and_paths: Dict[str, str]
    schema_directory: str
    extensions: List[str] = field(default_factory=list)

    @property
    def type(self):
        return "sqlite"

    def _connection_keys(self):
        """ Keys to show when debugging """
        return ["database", "schema", "schemas_and_paths", "schema_directory" ]


class SQLiteConnectionManager(SQLConnectionManager):
    TYPE = "sqlite"

    @classmethod
    def open(cls, connection: Connection):
        if connection.state == "open":
            logger.debug("Connection is already open, skipping open.")
            return connection

        credentials: SQLiteCredentials = connection.credentials

        schemas_and_paths = {}
        for schema, path in credentials.schemas_and_paths.items():
            # Make .db file path absolute
            schemas_and_paths[schema] = os.path.abspath(path)

        try:
            if 'main' in schemas_and_paths:
                handle: sqlite3.Connection = sqlite3.connect(schemas_and_paths['main'])
            else:
                raise FailedToConnectException("at least one schema must be called 'main'")

            if len(credentials.extensions) > 0:
                handle.enable_load_extension(True)

            for ext_path in credentials.extensions:
                handle.load_extension(ext_path)
            
            cursor = handle.cursor()

            attached = []
            for schema in set(schemas_and_paths.keys()) - set(['main']):
                path = schemas_and_paths[schema]
                cursor.execute(f"attach '{path}' as '{schema}'")
                attached.append(schema)

            for path in glob.glob(os.path.join(credentials.schema_directory, "*.db")):
                abs_path = os.path.abspath(path)

                # if file was already attached from being defined in schemas_and_paths, ignore it
                if not abs_path in schemas_and_paths.values():
                    schema = os.path.basename(path)[:-3]

                    # has schema name been used already?
                    if schema not in attached:
                        cursor.execute(f"attach '{path}' as '{schema}'")
                    else:
                        raise FailedToConnectException(
                            f"found {path} while scanning schema_directory, but cannot attach it as '{schema}' " +
                            f"because that schema name is already defined in schemas_and_paths. " +
                            f"fix your ~/.dbt/profiles.yml file")

            # # uncomment these lines to print out SQL: this only happens if statement is successful
            # handle.set_trace_callback(print)
            # sqlite3.enable_callback_tracebacks(True)

            connection.state = "open"
            connection.handle = handle

            return connection
        except sqlite3.Error as e:
            logger.debug(
                "Got an error when attempting to open a sqlite3 connection: '%s'", e
            )
            connection.handle = None
            connection.state = "fail"

            raise FailedToConnectException(str(e))
        except Exception as e:
            print(f"Unknown error opening SQLite connection: {e}")
            raise e

    @classmethod
    def get_status(cls, cursor: sqlite3.Cursor):
        return f"OK"#  {cursor.rowcount}"


    def get_response(cls, cursor) -> AdapterResponse:
        """
        new to support dbt 0.19: this method replaces get_response
        """
        message = 'OK'
        rows = cursor.rowcount
        return AdapterResponse(
            _message=message,
            rows_affected=rows
        )


    def cancel(self, connection):
        """ cancel ongoing queries """

        logger.debug("Cancelling queries")
        try:
            connection.handle.interrupt()
        except sqlite3.Error:
            pass
        logger.debug("Queries canceled")

    @contextmanager
    def exception_handler(self, sql: str):
        try:
            yield
        except sqlite3.DatabaseError as e:
            self.release()
            logger.debug("sqlite3 error: {}".format(str(e)))
            raise DatabaseException(str(e))
        except Exception as e:
            logger.debug("Error running SQL: {}".format(sql))
            logger.debug("Rolling back transaction.")
            self.release()
            raise RuntimeException(str(e))

    def add_query(
        self,
        sql: str,
        auto_begin: bool = True,
        bindings: Optional[Any] = None,
        abridge_sql_log: bool = False
    ) -> Tuple[Connection, Any]:
        """
        sqlite3's cursor.execute() doesn't like None as the
        bindings argument, so substitute an empty dict
        """
        if not bindings:
            bindings = {}

        return super().add_query(sql=sql, auto_begin=auto_begin, bindings=bindings, abridge_sql_log=abridge_sql_log)

