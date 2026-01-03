from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Expense
from datetime import datetime

# Create expenses blueprint
expense_bp = Blueprint('expense', __name__, url_prefix='/expense')


@expense_bp.route('/')
@login_required
def list_expenses():
    """
    Display all expenses for the current user.
    Expenses are ordered by date (most recent first).
    """
    expenses = Expense.query.filter_by(user_id=current_user.id)\
                            .order_by(Expense.date.desc())\
                            .all()
    return render_template('expense/list.html', expenses=expenses)


@expense_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    """
    Add a new expense.
    GET: Display add expense form
    POST: Process form and create new expense
    """
    if request.method == 'POST':
        category = request.form.get('category', '').strip()
        amount = request.form.get('amount', '').strip()
        date_str = request.form.get('date', '').strip()
        notes = request.form.get('notes', '').strip()
        
        # Validation
        if not category or not amount or not date_str:
            flash('Category, amount, and date are required.', 'danger')
            return redirect(url_for('expense.add_expense'))
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            flash('Amount must be a positive number.', 'danger')
            return redirect(url_for('expense.add_expense'))
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format.', 'danger')
            return redirect(url_for('expense.add_expense'))
        
        # Create new expense
        new_expense = Expense(
            user_id=current_user.id,
            category=category,
            amount=amount,
            date=date,
            notes=notes if notes else None
        )
        
        try:
            db.session.add(new_expense)
            db.session.commit()
            flash('Expense added successfully!', 'success')
            return redirect(url_for('expense.list_expenses'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the expense.', 'danger')
            return redirect(url_for('expense.add_expense'))
    
    # GET request: display add form
    return render_template('expense/add.html')


@expense_bp.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    """
    Edit an existing expense.
    GET: Display edit form with pre-filled data
    POST: Update the expense
    """
    expense = Expense.query.get_or_404(expense_id)
    
    # Security check: ensure user owns this expense
    if expense.user_id != current_user.id:
        flash('You do not have permission to edit this expense.', 'danger')
        return redirect(url_for('expense.list_expenses'))
    
    if request.method == 'POST':
        category = request.form.get('category', '').strip()
        amount = request.form.get('amount', '').strip()
        date_str = request.form.get('date', '').strip()
        notes = request.form.get('notes', '').strip()
        
        # Validation
        if not category or not amount or not date_str:
            flash('Category, amount, and date are required.', 'danger')
            return redirect(url_for('expense.edit_expense', expense_id=expense_id))
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            flash('Amount must be a positive number.', 'danger')
            return redirect(url_for('expense.edit_expense', expense_id=expense_id))
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format.', 'danger')
            return redirect(url_for('expense.edit_expense', expense_id=expense_id))
        
        # Update expense
        expense.category = category
        expense.amount = amount
        expense.date = date
        expense.notes = notes if notes else None
        
        try:
            db.session.commit()
            flash('Expense updated successfully!', 'success')
            return redirect(url_for('expense.list_expenses'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the expense.', 'danger')
            return redirect(url_for('expense.edit_expense', expense_id=expense_id))
    
    # GET request: display edit form with current data
    return render_template('expense/edit.html', expense=expense)


@expense_bp.route('/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    """
    Delete an expense.
    Only accepts POST requests for security.
    """
    expense = Expense.query.get_or_404(expense_id)
    
    # Security check: ensure user owns this expense
    if expense.user_id != current_user.id:
        flash('You do not have permission to delete this expense.', 'danger')
        return redirect(url_for('expense.list_expenses'))
    
    try:
        db.session.delete(expense)
        db.session.commit()
        flash('Expense deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the expense.', 'danger')
    
    return redirect(url_for('expense.list_expenses'))