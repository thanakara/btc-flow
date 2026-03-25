from unittest.mock import patch

import pytest

from btc_flow.etl.load import FIELDS, load_postgres


@patch("btc_flow.etl.load.psycopg2.connect")
def test_load_postgres_connects_with_correct_params(mock_connect, mock_conn, pg_cfg, transformed_record):
    mock_connect.return_value = mock_conn
    load_postgres(cfg=pg_cfg, record=transformed_record)
    mock_connect.assert_called_once_with(
        host="localhost",
        port=5432,
        dbname="btcflow",
        user="btcflow",
        password="btcflow",
    )


@patch("btc_flow.etl.load.psycopg2.connect")
def test_load_postgres_creates_table(mock_connect, mock_conn, pg_cfg, transformed_record):
    mock_connect.return_value = mock_conn
    load_postgres(cfg=pg_cfg, record=transformed_record)
    cur = mock_conn.cursor.return_value
    first_call = cur.execute.call_args_list[0]
    assert "CREATE TABLE IF NOT EXISTS" in first_call[0][0]


@patch("btc_flow.etl.load.psycopg2.connect")
def test_load_postgres_inserts_record(mock_connect, mock_conn, pg_cfg, transformed_record):
    mock_connect.return_value = mock_conn
    load_postgres(cfg=pg_cfg, record=transformed_record)
    cur = mock_conn.cursor.return_value
    second_call = cur.execute.call_args_list[1]
    assert "INSERT INTO" in second_call[0][0]
    assert second_call[0][1] == [transformed_record[f] for f in FIELDS]


@patch("btc_flow.etl.load.psycopg2.connect")
def test_load_postgres_closes_connection(mock_connect, mock_conn, pg_cfg, transformed_record):
    mock_connect.return_value = mock_conn
    load_postgres(cfg=pg_cfg, record=transformed_record)
    mock_conn.close.assert_called_once()


@patch("btc_flow.etl.load.psycopg2.connect")
def test_load_postgres_closes_connection_on_error(mock_connect, mock_conn, pg_cfg, transformed_record):
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value.execute.side_effect = Exception("DB error")
    with pytest.raises(Exception, match="DB error"):
        load_postgres(cfg=pg_cfg, record=transformed_record)
    mock_conn.close.assert_called_once()
