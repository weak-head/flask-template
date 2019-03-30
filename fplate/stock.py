from flask import (Blueprint, jsonify, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort

from fplate.auth import login_required
from fplate.db import get_db

bp = Blueprint('stock', __name__)

@bp.route('/', methods=['GET'])
def get_all():
    db = get_db()
    query = ('SELECT symbol, company, total_count, price '
             'FROM stock')
    stocks = db.execute(query).fetchall()
    return jsonify(stocks)


@bp.route('/<string:symbol>', methods=['GET'])
def get(symbol):
    stock = get_stock(symbol)
    return jsonify(stock)


def get_stock(symbol):
    db = get_db()
    query = ('SELECT symbol, company, total_count, price '
             'FROM stock '
             'WHERE symbol = ?')
    stock = db.execute(query, (symbol,)).fetchall()

    if stock is None:
        abort(404, "Stock {stock} doesn't exist".format(stock=stock))

    return stock

