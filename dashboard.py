from flask import Blueprint, render_template
from flask_login import login_required, current_user
from decimal import Decimal
from .models import Holding, Transaction, User
from .api_client import get_realtime_price

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def index():
    user = User.query.get(current_user.id)
    holdings = Holding.query.filter_by(user_id=user.id).all()
    transactions = Transaction.query.filter_by(
        user_id=user.id
    ).order_by(Transaction.timestamp.desc()).limit(10)

    # Simple aggregation
    total_value = Decimal("0")
    allocation = []
    for h in holdings:
        price = get_realtime_price(h.symbol) or h.avg_price
        value = price * h.quantity
        total_value += value
        allocation.append({"symbol": h.symbol, "value": float(value)})

    net_worth = total_value + user.cash_balance

    return render_template(
        "dashboard.html",
        net_worth=net_worth,
        cash=user.cash_balance,
        total_value=total_value,
        allocation=allocation,
        transactions=transactions
    )
