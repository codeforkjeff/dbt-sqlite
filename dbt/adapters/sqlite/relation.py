from dataclasses import dataclass, field

from dbt.adapters.base.relation import BaseRelation, Policy


@dataclass
class SQLiteQuotePolicy(Policy):
    database: bool = False
    schema: bool = False
    identifier: bool = True


@dataclass
class SQLiteIncludePolicy(Policy):
    database: bool = False
    schema: bool = True
    identifier: bool = True


@dataclass(frozen=True, eq=False, repr=False)
class SQLiteRelation(BaseRelation):
    quote_policy: SQLiteQuotePolicy = field(default_factory=SQLiteQuotePolicy)
    include_policy: SQLiteIncludePolicy = field(default_factory=SQLiteIncludePolicy)
