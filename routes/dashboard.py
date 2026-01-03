from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from models import db, StudySession, Expense
from datetime import datetime, timedelta
from sqlalchemy import func

# Create dashboard blueprint
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


def get_week_range():
    """Calculate start and end dates for the current week (Monday to Sunday)."""
    today = datetime.now().date()
    start = today - timedelta(days=today.weekday())  # Monday
    end = start + timedelta(days=6)  # Sunday
    return start, end


def get_month_range():
    """Calculate start and end dates for the current month."""
    today = datetime.now().date()
    start = today.replace(day=1)
    # Calculate last day of month
    next_month = start.replace(day=28) + timedelta(days=4)
    end = (next_month - timedelta(days=next_month.day))
    return start, end


def get_quarter_range():
    """Calculate start and end dates for the current quarter."""
    today = datetime.now().date()
    quarter = (today.month - 1) // 3  # 0, 1, 2, or 3
    start_month = quarter * 3 + 1
    start = today.replace(month=start_month, day=1)
    
    # Calculate end of quarter
    end_month = start_month + 2
    if end_month <= 12:
        end = today.replace(month=end_month, day=1)
        next_month = end + timedelta(days=32)
        end = next_month.replace(day=1) - timedelta(days=1)
    else:
        end = today.replace(month=12, day=31)
    
    return start, end


@dashboard_bp.route('/')
@login_required
def index():
    """
    Main dashboard view.
    Displays summary statistics and renders the dashboard template.
    """
    # Get date ranges
    week_start, week_end = get_week_range()
    month_start, month_end = get_month_range()
    quarter_start, quarter_end = get_quarter_range()
    
    # Calculate weekly totals
    weekly_study = db.session.query(func.sum(StudySession.duration))\
        .filter(StudySession.user_id == current_user.id)\
        .filter(StudySession.date.between(week_start, week_end))\
        .scalar() or 0
    
    weekly_expenses = db.session.query(func.sum(Expense.amount))\
        .filter(Expense.user_id == current_user.id)\
        .filter(Expense.date.between(week_start, week_end))\
        .scalar() or 0.0
    
    # Calculate monthly totals
    monthly_study = db.session.query(func.sum(StudySession.duration))\
        .filter(StudySession.user_id == current_user.id)\
        .filter(StudySession.date.between(month_start, month_end))\
        .scalar() or 0
    
    monthly_expenses = db.session.query(func.sum(Expense.amount))\
        .filter(Expense.user_id == current_user.id)\
        .filter(Expense.date.between(month_start, month_end))\
        .scalar() or 0.0
    
    # Calculate quarterly totals
    quarterly_study = db.session.query(func.sum(StudySession.duration))\
        .filter(StudySession.user_id == current_user.id)\
        .filter(StudySession.date.between(quarter_start, quarter_end))\
        .scalar() or 0
    
    quarterly_expenses = db.session.query(func.sum(Expense.amount))\
        .filter(Expense.user_id == current_user.id)\
        .filter(Expense.date.between(quarter_start, quarter_end))\
        .scalar() or 0.0
    
    # Pass data to template
    return render_template('dashboard/dashboard.html',
                         weekly_study=weekly_study,
                         weekly_expenses=round(weekly_expenses, 2),
                         monthly_study=monthly_study,
                         monthly_expenses=round(monthly_expenses, 2),
                         quarterly_study=quarterly_study,
                         quarterly_expenses=round(quarterly_expenses, 2),
                         week_start=week_start,
                         week_end=week_end,
                         month_start=month_start,
                         month_end=month_end,
                         quarter_start=quarter_start,
                         quarter_end=quarter_end)


@dashboard_bp.route('/chart-data/<period>')
@login_required
def chart_data(period):
    """
    API endpoint to fetch chart data for a specific period.
    Returns JSON with daily aggregated study time and expenses.
    Periods: 'week', 'month', 'quarter'
    """
    # Determine date range based on period
    if period == 'week':
        start, end = get_week_range()
    elif period == 'month':
        start, end = get_month_range()
    elif period == 'quarter':
        start, end = get_quarter_range()
    else:
        return jsonify({'error': 'Invalid period'}), 400
    
    # Query daily study totals
    study_data = db.session.query(
        StudySession.date,
        func.sum(StudySession.duration).label('total')
    ).filter(StudySession.user_id == current_user.id)\
     .filter(StudySession.date.between(start, end))\
     .group_by(StudySession.date)\
     .all()
    
    # Query daily expense totals
    expense_data = db.session.query(
        Expense.date,
        func.sum(Expense.amount).label('total')
    ).filter(Expense.user_id == current_user.id)\
     .filter(Expense.date.between(start, end))\
     .group_by(Expense.date)\
     .all()
    
    # Create dictionaries for easier lookup
    study_dict = {str(item.date): int(item.total) for item in study_data}
    expense_dict = {str(item.date): float(item.total) for item in expense_data}
    
    # Generate all dates in range
    dates = []
    current_date = start
    while current_date <= end:
        date_str = str(current_date)
        dates.append({
            'date': date_str,
            'study': study_dict.get(date_str, 0),
            'expense': round(expense_dict.get(date_str, 0.0), 2)
        })
        current_date += timedelta(days=1)
    
    return jsonify(dates)