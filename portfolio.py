from flask import Blueprint, render_template
from flask_login import login_required, current_user
from decimal import Decimal
from .models import Holding, Transaction, User
from .api_client import get_realtime_price

portfolio_bp = Blueprint("portfolio", __name__)

@portfolio_bp.route("/")
@login_required
def view_portfolio():
    user = User.query.get(current_user.id)
    holdings = Holding.query.filter_by(user_id=user.id).all()

    rows = []
    total_value = Decimal("0")
    total_cost = Decimal("0")

    for h in holdings:
        price = get_realtime_price(h.symbol) or h.avg_price
        market_value = price * h.quantity
        cost_basis = h.avg_price * h.quantity
        unrealized_pnl = market_value - cost_basis
        total_value += market_value
        total_cost += cost_basis

        rows.append({
            "symbol": h.symbol,
            "quantity": h.quantity,
            "avg_price": h.avg_price,
            "price": price,
            "market_value": market_value,
            "unrealized_pnl": unrealized_pnl
        })

    total_pnl = total_value - total_cost
    net_worth = total_value + user.cash_balance

    return render_template(
        "portfolio.html",
        holdings=rows,
        cash=user.cash_balance,
        total_value=total_value,
        total_pnl=total_pnl,
        net_worth=net_worth
    )
