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


@bp.route('/<string:symbol>/update', method=['PATCH'])
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
    get_stock(symbol)
    db = get_db()
    db.execute('DELETE * FROM stock WHERE symbol = ?', [symbol])
    db.commit()
    return make_response('OK', 200)


@bp.route('/<string:symbol>', methods=['GET'])
def get(symbol):
    stock = get_stock(symbol)
    return jsonify(stock)


@bp.route('/', methods=['GET'])
def get_all():
    db = get_db()
    query = ('SELECT symbol, company, total_count, price '
             'FROM stock')
    stocks = db.execute(query).fetchall()
    return jsonify(stocks)


def get_stock(symbol):
    db = get_db()
    query = ('SELECT symbol, company, total_count, price '
             'FROM stock '
             'WHERE symbol = ?')
    stock = db.execute(query, (symbol,)).fetchall()

    if stock is None:
        abort(404, "Stock {stock} doesn't exist".format(stock=stock))

    return stock
