from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, StudySession
from datetime import datetime

# Create study sessions blueprint
study_bp = Blueprint('study', __name__, url_prefix='/study')


@study_bp.route('/')
@login_required
def list_sessions():
    """
    Display all study sessions for the current user.
    Sessions are ordered by date (most recent first).
    """
    sessions = StudySession.query.filter_by(user_id=current_user.id)\
                                  .order_by(StudySession.date.desc())\
                                  .all()
    return render_template('study/list.html', sessions=sessions)


@study_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_session():
    """
    Add a new study session.
    GET: Display add session form
    POST: Process form and create new session
    """
    if request.method == 'POST':
        subject = request.form.get('subject', '').strip()
        duration = request.form.get('duration', '').strip()
        date_str = request.form.get('date', '').strip()
        notes = request.form.get('notes', '').strip()
        
        # Validation
        if not subject or not duration or not date_str:
            flash('Subject, duration, and date are required.', 'danger')
            return redirect(url_for('study.add_session'))
        
        try:
            duration = int(duration)
            if duration <= 0:
                raise ValueError("Duration must be positive")
        except ValueError:
            flash('Duration must be a positive number.', 'danger')
            return redirect(url_for('study.add_session'))
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format.', 'danger')
            return redirect(url_for('study.add_session'))
        
        # Create new study session
        new_session = StudySession(
            user_id=current_user.id,
            subject=subject,
            duration=duration,
            date=date,
            notes=notes if notes else None
        )
        
        try:
            db.session.add(new_session)
            db.session.commit()
            flash('Study session added successfully!', 'success')
            return redirect(url_for('study.list_sessions'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the session.', 'danger')
            return redirect(url_for('study.add_session'))
    
    # GET request: display add form
    return render_template('study/add.html')


@study_bp.route('/edit/<int:session_id>', methods=['GET', 'POST'])
@login_required
def edit_session(session_id):
    """
    Edit an existing study session.
    GET: Display edit form with pre-filled data
    POST: Update the session
    """
    session = StudySession.query.get_or_404(session_id)
    
    # Security check: ensure user owns this session
    if session.user_id != current_user.id:
        flash('You do not have permission to edit this session.', 'danger')
        return redirect(url_for('study.list_sessions'))
    
    if request.method == 'POST':
        subject = request.form.get('subject', '').strip()
        duration = request.form.get('duration', '').strip()
        date_str = request.form.get('date', '').strip()
        notes = request.form.get('notes', '').strip()
        
        # Validation
        if not subject or not duration or not date_str:
            flash('Subject, duration, and date are required.', 'danger')
            return redirect(url_for('study.edit_session', session_id=session_id))
        
        try:
            duration = int(duration)
            if duration <= 0:
                raise ValueError("Duration must be positive")
        except ValueError:
            flash('Duration must be a positive number.', 'danger')
            return redirect(url_for('study.edit_session', session_id=session_id))
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format.', 'danger')
            return redirect(url_for('study.edit_session', session_id=session_id))
        
        # Update session
        session.subject = subject
        session.duration = duration
        session.date = date
        session.notes = notes if notes else None
        
        try:
            db.session.commit()
            flash('Study session updated successfully!', 'success')
            return redirect(url_for('study.list_sessions'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the session.', 'danger')
            return redirect(url_for('study.edit_session', session_id=session_id))
    
    # GET request: display edit form with current data
    return render_template('study/edit.html', session=session)


@study_bp.route('/delete/<int:session_id>', methods=['POST'])
@login_required
def delete_session(session_id):
    """
    Delete a study session.
    Only accepts POST requests for security.
    """
    session = StudySession.query.get_or_404(session_id)
    
    # Security check: ensure user owns this session
    if session.user_id != current_user.id:
        flash('You do not have permission to delete this session.', 'danger')
        return redirect(url_for('study.list_sessions'))
    
    try:
        db.session.delete(session)
        db.session.commit()
        flash('Study session deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the session.', 'danger')
    
    return redirect(url_for('study.list_sessions'))