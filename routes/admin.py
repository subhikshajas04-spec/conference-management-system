from flask import Blueprint, render_template, redirect, url_for, flash, session
from models import db, User, Conference, Paper

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        flash('Access Denied! Only Admin can access this.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    users = User.query.all()
    conferences = Conference.query.all()
    papers = Paper.query.all()
    
    return render_template('admin/dashboard.html', 
                         users=users, 
                         conferences=conferences, 
                         papers=papers)

@admin_bp.route('/admin/delete_user/<int:user_id>')
def delete_user(user_id):
    if session.get('role') != 'admin':
        flash('Access Denied!', 'danger')
        return redirect(url_for('main.dashboard'))
    
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash('Cannot delete admin account!', 'danger')
        return redirect(url_for('admin.admin_dashboard'))
    
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/delete_conference/<int:conf_id>')
def delete_conference(conf_id):
    if session.get('role') != 'admin':
        flash('Access Denied!', 'danger')
        return redirect(url_for('main.dashboard'))
    
    conference = Conference.query.get_or_404(conf_id)
    db.session.delete(conference)
    db.session.commit()
    flash('Conference deleted successfully!', 'success')
    return redirect(url_for('admin.admin_dashboard'))