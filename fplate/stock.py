import json

from flask import (Blueprint, jsonify, flash, g, request, make_response)
from werkzeug.exceptions import abort

from fplate.auth import login_required
from fplate.db import get_db

bp = Blueprint('stock', __name__, url_prefix='/stock')


@bp.route('/create', methods=['POST'])
@login_required
def create():
    req_json = request.get_json()
    symbol = req_json['symbol']
    company = req_json['company']
    total_count = req_json['total_count']
    price = req_json['price']

    if get_stock(symbol) is not None:
        return make_response('already exist', 409)

    db = get_db()
    db.execute(
        'INSERT INTO stock (symbol, company, total_count, price) '
        'VALUES (?, ?, ?, ?)', (symbol, company, total_count, price))
    db.commit()

    return make_response('Created', 201)


@bp.route('/<string:symbol>/update', methods=['PATCH'])
@login_required
def update(symbol):
    rj = request.get_json()
    company = rj['company']
    total_count = rj['total_count']
    price = rj['price']

    if get_stock(symbol) is None:
        return make_response('Does not exist', 404)

    db = get_db()
    db.execute(
        'UPDATE stock '
        'SET company = ?, total_count = ?, price = ? '
        'WHERE symbol = ?',
        (company, total_count, price, symbol))
    db.commit()

    return make_response('Updated', 200)


@bp.route('/<string:symbol>/delete', methods=['DELETE'])
@login_required
def delete(symbol):
    if get_stock(symbol) is None:
        return make_response('Not found', 404)

    db = get_db()
    db.execute('DELETE FROM stock WHERE symbol = ?', (symbol,))
    db.commit()

    return make_response('OK', 200)


@bp.route('/<string:symbol>', methods=['GET'])
def get(symbol):
    stock = get_stock(symbol)
    return json.dumps(stock) if stock else make_response('Not found', 404)


@bp.route('/', methods=['GET'])
def get_all():
    cursor = get_db().cursor()
    query = ('SELECT symbol, company, total_count, price '
             'FROM stock')
    rows = cursor.execute(query).fetchall()
    cursor.close()

    return json.dumps([dict(ix) for ix in rows])


def get_stock(symbol):
    cursor = get_db().cursor()
    query = ('SELECT symbol, company, total_count, price '
             'FROM stock '
             'WHERE symbol = ?')
    stock = cursor.execute(query, [symbol]).fetchall()
    cursor.close()

    return [dict(ix) for ix in stock] if stock else None
