from pandas import DataFrame
import streamlit as st
from duckdb import DuckDBPyConnection, connect

from exposition.tables import Table
from src.logger.log_handler import log


@st.cache_resource
def get_connection(database: str) -> DuckDBPyConnection:
    log.info("Connecting to DuckDB database: %s", database)
    return connect(database, read_only=True)


@st.cache_data
def fetch_data(tables: list[Table]) -> dict[str, DataFrame]:
    results = {}
    for table in tables:
        conn = get_connection(table.database)
        query = f"SELECT {', '.join(table.columns)} FROM {table.schema}.{table.name}"
        df = conn.execute(query).df()
        log.info("Fetched data from %s.%s", table.schema, table.name)
        results[table.name] = df
    return results
