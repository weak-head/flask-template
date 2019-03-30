import functools
from flask import (Blueprint, flash, g, request,
                   session, url_for, make_response)
from werkzeug.security import check_password_hash, generate_password_hash
from fplate.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        req_json = request.get_json()
        username = req_json['username']
        password = req_json['password']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return make_response('', 200)

        flash(error)

    return make_response('err', 401)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        req_json = request.get_json()
        username = req_json['username']
        password = req_json['password']

        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # JWT
            session.clear()
            session['user_id'] = user['id']
            return make_response('OK', 200)

        flash(error)

    return make_response('NG', 401)


@bp.route('/logout')
def logout():
    session.clear()
    return make_response('OK', 200)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return make_response('failed', 400)

        return view(**kwargs)

    return wrapped_view
