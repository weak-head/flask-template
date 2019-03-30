import pytest
import json
from flask import g, session
from fplate.db import get_db


def test_register(client, app):
    response = client.post(
        '/auth/register',
        data=json.dumps({'username': 'a', 'password': 'a'}),
        content_type='application/json'
    )
    assert response.status_code == 201
    assert response.data == b'Created'

    with app.app_context():
        assert get_db().execute(
            "select * from user where username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data=json.dumps({'username': username, 'password': password}),
        content_type='application/json'
    )
    assert message in response.data


def test_login(client, auth):
    response = auth.login()
    assert response.status_code == 200

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
