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


def test_get_existing(client, app):
    resp = client.get('/stock/AAB')

    assert resp.status_code == 200
    stocks = json.loads(resp.data)

    assert len(stocks) == 1
    assert stocks[0]['symbol'] == 'AAB'
    assert stocks[0]['company'] == 'abbybaba'
    assert stocks[0]['total_count'] == 12
    assert stocks[0]['price'] == 140


def test_get_non_existing(client, app):
    resp = client.get('/stock/DEF')
    assert resp.status_code == 404
    assert resp.data == b'Not found'


def test_delete_no_auth(client, app, auth):
    resp = client.delete('/stock/AAB/delete')
    assert resp.status_code == 401
    assert resp.data == b'Unauthorized'


def test_delete_non_existing(client, app, auth):
    auth.login()
    resp = client.delete('/stock/DEF/delete')
    assert resp.status_code == 404
    assert resp.data == b'Not found'


def test_delete_existing(client, app, auth):
    auth.login()

    resp = client.get('/stock/AAB')
    assert resp.status_code == 200

    resp = client.delete('/stock/AAB/delete')
    assert resp.status_code == 200
    assert resp.data == b'OK'

    resp = client.get('/stock/AAB')
    assert resp.status_code == 404
    assert resp.data == b'Not found'
