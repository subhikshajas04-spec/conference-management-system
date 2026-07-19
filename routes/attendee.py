from flask import Blueprint, render_template, redirect, url_for, flash, session
from models import db, Conference, Registration   # ← db is imported here

attendee_bp = Blueprint('attendee', __name__)

@attendee_bp.route('/browse_conferences')
def browse_conferences():
    if session.get('role') != 'attendee':
        flash('Access Denied! Only attendees can browse conferences.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    conferences = Conference.query.all()
    return render_template('attendee/browse_conferences.html', conferences=conferences)

@attendee_bp.route('/register_conference/<int:conf_id>')
def register_conference(conf_id):
    if 'user_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('auth.login'))
    
    # Check if already registered
    existing = Registration.query.filter_by(conference_id=conf_id, user_id=session['user_id']).first()
    if existing:
        flash('You are already registered for this conference!', 'info')
        return redirect(url_for('attendee.browse_conferences'))
    
    registration = Registration(conference_id=conf_id, user_id=session['user_id'])
    db.session.add(registration)
    db.session.commit()
    
    flash('Successfully registered for the conference!', 'success')
    return redirect(url_for('attendee.browse_conferences'))