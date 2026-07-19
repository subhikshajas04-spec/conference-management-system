from flask import Blueprint, render_template, session, redirect, url_for, request
from models import Conference, Paper, Registration

main_bp = Blueprint('main', __name__)

# ====================== HOME PAGE (Landing Page with Get Started) ======================
@main_bp.route('/')
def index():
    return render_template('index.html')        # This will show your nice landing page

# ====================== DASHBOARD ======================
@main_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    role = session.get('role')
    name = session.get('name')
    
    conferences = []
    papers = []
    total_papers = 0
    accepted_papers = 0
    total_attendees = 0

    if role == 'organizer':
        conferences = Conference.query.filter_by(organizer_id=session['user_id']).all()
        
        for conf in conferences:
            conf_papers = Paper.query.filter_by(conference_id=conf.id).all()
            total_papers += len(conf_papers)
            accepted_papers += len([p for p in conf_papers if p.status == 'accepted'])
        
        # Count attendees for organizer's conferences
        total_attendees = Registration.query.join(Conference).filter(
            Conference.organizer_id == session['user_id']
        ).count()

    elif role == 'author':
        papers = Paper.query.filter_by(author_id=session['user_id']).all()

    return render_template('dashboard.html', 
                           role=role, 
                           name=name,
                           conferences=conferences,
                           papers=papers,
                           total_papers=total_papers,
                           accepted_papers=accepted_papers,
                           total_attendees=total_attendees)

# ====================== GLOBAL SEARCH ======================
@main_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    papers = []
    conferences = []
    
    if query:
        papers = Paper.query.filter(Paper.title.ilike(f'%{query}%')).all()
        conferences = Conference.query.filter(Conference.title.ilike(f'%{query}%')).all()
    
    return render_template('search.html', 
                         query=query, 
                         papers=papers, 
                         conferences=conferences)