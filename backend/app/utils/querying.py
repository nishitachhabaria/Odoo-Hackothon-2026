"""Reusable query helpers for search and sorting."""

from __future__ import annotations

from typing import Any

from sqlalchemy.sql.elements import ColumnElement


def resolve_sort_expression(
    sort: str,
    allowed_columns: dict[str, ColumnElement[Any]],
    default_key: str,
) -> ColumnElement[Any]:
    """Resolve a sort string into a SQLAlchemy order expression.

    The sort value may use a leading dash to request descending order.
    """

    descending = sort.startswith("-")
    sort_key = sort[1:] if descending else sort
    column = allowed_columns.get(sort_key, allowed_columns[default_key])
    return column.desc() if descending else column.asc()
