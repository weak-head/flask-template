import pytest
import json
from flask import g, session
from fplate.db import get_db


def test_get_all(client, app):
    resp = client.get('/stock/')

    assert resp.status_code == 200
    stocks = json.loads(resp.data)

    expected_data = [
        {'symbol': 'AAB', 'company': 'abbybaba', 'total_count': 12, 'price': 140},
        {'symbol': 'BBC', 'company': 'BbBbCc', 'total_count': 37, 'price': 42}
    ]

    assert len(expected_data) == len(stocks)
    for test_case in expected_data:
        assert test_case in stocks


def test_get(client, app):
    resp = client.get('/stock/AAB')

    assert resp.status_code == 200
    stocks = json.loads(resp.data)

    assert len(stocks) == 1
    assert stocks[0]['symbol'] == 'AAB'
    assert stocks[0]['company'] == 'abbybaba'
    assert stocks[0]['total_count'] == 12
    assert stocks[0]['price'] == 140
