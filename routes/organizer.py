from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
from models import db, Conference, Paper, User, PaperAssignment, Review, Registration, PresentationSchedule
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

organizer_bp = Blueprint('organizer', __name__)

# ====================== CREATE CONFERENCE ======================
@organizer_bp.route('/create_conference', methods=['GET', 'POST'])
def create_conference():
    if session.get('role') != 'organizer':
        flash('Access Denied!', 'danger')
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        try:
            start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
            conference = Conference(
                title=request.form['title'],
                description=request.form.get('description', ''),
                organizer_id=session['user_id'],
                start_date=start_date,
                end_date=end_date,
                location=request.form['location']
            )
            db.session.add(conference)
            db.session.commit()
            flash('Conference created successfully!', 'success')
            return redirect(url_for('organizer.my_conferences'))
        except Exception as e:
            flash('Error creating conference.', 'danger')
    return render_template('organizer/create_conference.html')

# ====================== MY CONFERENCES ======================
@organizer_bp.route('/my_conferences')
def my_conferences():
    if session.get('role') != 'organizer':
        flash('Access Denied!', 'danger')
        return redirect(url_for('main.dashboard'))
    conferences = Conference.query.filter_by(organizer_id=session['user_id']).all()
    return render_template('organizer/my_conferences.html', conferences=conferences)

# ====================== MANAGE PAPERS ======================
@organizer_bp.route('/manage_papers/<int:conf_id>')
def manage_papers(conf_id):
    if session.get('role') != 'organizer':
        flash('Access Denied!', 'danger')
        return redirect(url_for('main.dashboard'))
    conference = Conference.query.get_or_404(conf_id)
    if conference.organizer_id != session.get('user_id'):
        flash('Access Denied!', 'danger')
        return redirect(url_for('organizer.my_conferences'))
    papers = Paper.query.filter_by(conference_id=conf_id).all()
    return render_template('organizer/manage_papers.html', conference=conference, papers=papers)

# ====================== UPDATE PAPER STATUS ======================
@organizer_bp.route('/update_paper_status/<int:paper_id>', methods=['POST'])
def update_paper_status(paper_id):
    if session.get('role') != 'organizer':
        flash('Access Denied!', 'danger')
        return redirect(url_for('main.dashboard'))
    paper = Paper.query.get_or_404(paper_id)
    paper.status = request.form.get('status')
    db.session.commit()
    flash(f'Paper status updated to {paper.status.upper()}!', 'success')
    return redirect(request.referrer or url_for('main.dashboard'))

# ====================== ASSIGN REVIEWER ======================
@organizer_bp.route('/assign_reviewer/<int:paper_id>', methods=['GET', 'POST'])
def assign_reviewer(paper_id):
    if session.get('role') != 'organizer':
        flash('Access Denied!', 'danger')
        return redirect(url_for('main.dashboard'))
    paper = Paper.query.get_or_404(paper_id)
    conference = Conference.query.get(paper.conference_id)
    if conference.organizer_id != session.get('user_id'):
        flash('Access Denied!', 'danger')
        return redirect(url_for('organizer.my_conferences'))
    reviewers = User.query.filter_by(role='reviewer').all()
    if request.method == 'POST':
        reviewer_id = int(request.form['reviewer_id'])
        existing = PaperAssignment.query.filter_by(paper_id=paper_id, reviewer_id=reviewer_id).first()
        if existing:
            flash('Reviewer already assigned!', 'info')
            return redirect(url_for('organizer.manage_papers', conf_id=paper.conference_id))
        assignment = PaperAssignment(paper_id=paper_id, reviewer_id=reviewer_id)
        db.session.add(assignment)
        db.session.commit()
        flash('Reviewer assigned successfully!', 'success')
        return redirect(url_for('organizer.manage_papers', conf_id=paper.conference_id))
    return render_template('organizer/assign_reviewer.html', paper=paper, reviewers=reviewers)

# ====================== VIEW REVIEWS ======================
@organizer_bp.route('/view_reviews/<int:paper_id>')
def view_reviews(paper_id):
    if session.get('role') != 'organizer':
        flash('Access Denied!', 'danger')
        return redirect(url_for('main.dashboard'))
    paper = Paper.query.get_or_404(paper_id)
    conference = Conference.query.get(paper.conference_id)
    if conference.organizer_id != session.get('user_id'):
        flash('Access Denied!', 'danger')
        return redirect(url_for('organizer.my_conferences'))
    reviews = Review.query.filter_by(paper_id=paper_id).all()
    return render_template('organizer/view_reviews.html', paper=paper, reviews=reviews)

# ====================== VIEW ATTENDEES ======================
@organizer_bp.route('/view_attendees/<int:conf_id>')
def view_attendees(conf_id):
    if session.get('role') != 'organizer':
        flash('Access Denied!', 'danger')
        return redirect(url_for('main.dashboard'))
    conference = Conference.query.get_or_404(conf_id)
    if conference.organizer_id != session.get('user_id'):
        flash('Access Denied!', 'danger')
        return redirect(url_for('organizer.my_conferences'))
    registrations = Registration.query.filter_by(conference_id=conf_id).all()
    return render_template('organizer/view_attendees.html', conference=conference, registrations=registrations)

# ====================== SCHEDULE PRESENTATION ======================
@organizer_bp.route('/schedule_presentation/<int:paper_id>', methods=['GET', 'POST'])
def schedule_presentation(paper_id):
    if session.get('role') != 'organizer':
        flash('Access Denied!', 'danger')
        return redirect(url_for('main.dashboard'))
    paper = Paper.query.get_or_404(paper_id)
    conference = Conference.query.get(paper.conference_id)
    if conference.organizer_id != session.get('user_id'):
        flash('Access Denied!', 'danger')
        return redirect(url_for('organizer.my_conferences'))
    if paper.status != 'accepted':
        flash('Only accepted papers can be scheduled!', 'danger')
        return redirect(url_for('organizer.manage_papers', conf_id=paper.conference_id))
    if request.method == 'POST':
        session_date = datetime.strptime(request.form['session_date'], '%Y-%m-%d').date()
        session_time = datetime.strptime(request.form['session_time'], '%H:%M').time()
        session_title = request.form.get('session_title', 'Paper Presentation')
        schedule = PresentationSchedule(
            paper_id=paper_id,
            session_title=session_title,
            session_date=session_date,
            session_time=session_time
        )
        db.session.add(schedule)
        db.session.commit()
        flash(f'Presentation scheduled for {session_date} at {session_time}', 'success')
        return redirect(url_for('organizer.manage_papers', conf_id=paper.conference_id))
    from datetime import timedelta
    dates = []
    current = conference.start_date
    while current <= conference.end_date:
        dates.append(current)
        current += timedelta(days=1)
    return render_template('organizer/schedule_presentation.html', paper=paper, conference=conference, dates=dates)

# ====================== GENERATE CERTIFICATE ======================
@organizer_bp.route('/generate_certificate/<int:paper_id>')
def generate_certificate(paper_id):
    if session.get('role') != 'organizer':
        flash('Access Denied!', 'danger')
        return redirect(url_for('main.dashboard'))
    
    paper = Paper.query.get_or_404(paper_id)
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    p.setFont("Helvetica-Bold", 26)
    p.drawCentredString(300, 720, "Certificate of Presentation")
    
    p.setFont("Helvetica", 16)
    p.drawCentredString(300, 650, "This is to certify that")
    
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(300, 610, paper.title)
    
    p.setFont("Helvetica", 16)
    p.drawCentredString(300, 570, "was presented at the")
    p.drawCentredString(300, 540, "ConfHub International Conference")
    
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(300, 500, "on Artificial Intelligence 2026")
    
    p.setFont("Helvetica", 14)
    p.drawCentredString(300, 420, f"Date: {datetime.now().strftime('%d %B %Y')}")
    
    p.save()
    
    buffer.seek(0)
    return send_file(
        buffer, 
        as_attachment=True, 
        download_name=f"Certificate_{paper.id}.pdf",
        mimetype='application/pdf'
    )

# ====================== EXPORT SCHEDULE ======================
@organizer_bp.route('/export_schedule/<int:conf_id>')
def export_schedule(conf_id):
    if session.get('role') != 'organizer':
        flash('Access Denied!', 'danger')
        return redirect(url_for('main.dashboard'))
    
    conference = Conference.query.get_or_404(conf_id)
    papers = Paper.query.filter_by(conference_id=conf_id, status='accepted').all()
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(300, 750, f"Conference Schedule - {conference.title}")
    
    y = 700
    for paper in papers:
        if paper.schedule:
            p.setFont("Helvetica", 12)
            p.drawString(80, y, f"• {paper.schedule.session_date}  {paper.schedule.session_time}")
            p.drawString(280, y, paper.schedule.session_title)
            p.drawString(500, y, paper.title[:40])
            y -= 35
    p.save()
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"Schedule_{conf_id}.pdf", mimetype='application/pdf')