from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from decimal import Decimal
from .models import Holding, Transaction, User
from .api_client import get_realtime_price
from . import db

trading_bp = Blueprint("trading", __name__)

@trading_bp.route("/", methods=["GET", "POST"])
@login_required
def trade():
    if request.method == "POST":
        symbol = request.form["symbol"].upper()
        side = request.form["side"]  # BUY or SELL
        qty = Decimal(request.form["quantity"])

        price = get_realtime_price(symbol)
        if price is None:
            flash("Invalid symbol or price unavailable")
            return redirect(url_for("trading.trade"))

        user = User.query.get(current_user.id)

        if side == "BUY":
            cost = qty * price
            if user.cash_balance < cost:
                flash("Insufficient cash")
                return redirect(url_for("trading.trade"))

            user.cash_balance -= cost

            holding = Holding.query.filter_by(
                user_id=user.id, symbol=symbol
            ).first()
            if holding:
                total_qty = holding.quantity + qty
                holding.avg_price = (
                    (holding.avg_price * holding.quantity) + cost
                ) / total_qty
                holding.quantity = total_qty
            else:
                holding = Holding(
                    user_id=user.id,
                    symbol=symbol,
                    quantity=qty,
                    avg_price=price
                )
                db.session.add(holding)

        elif side == "SELL":
            holding = Holding.query.filter_by(
                user_id=user.id, symbol=symbol
            ).first()
            if not holding or holding.quantity < qty:
                flash("Not enough shares to sell")
                return redirect(url_for("trading.trade"))

            proceeds = qty * price
            user.cash_balance += proceeds
            holding.quantity -= qty
            if holding.quantity == 0:
                db.session.delete(holding)

        tx = Transaction(
            user_id=user.id,
            symbol=symbol,
            side=side,
            quantity=qty,
            price=price
        )
        db.session.add(tx)
        db.session.commit()
        flash(f"{side} order executed for {qty} {symbol} at {price}")
        return redirect(url_for("trading.trade"))

    return render_template("trade.html")
