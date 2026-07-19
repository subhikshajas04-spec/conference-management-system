from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Paper, Conference
import os
import re

author_bp = Blueprint('author', __name__)

# ====================== SUBMIT PAPER ======================
@author_bp.route('/submit_paper', methods=['GET', 'POST'])
def submit_paper():
    if session.get('role') != 'author':
        flash('Access Denied!', 'danger')
        return redirect(url_for('main.dashboard'))
    
    conferences = Conference.query.all()
    
    if request.method == 'POST':
        title = request.form['title']
        abstract = request.form['abstract']
        keywords = request.form['keywords']
        conf_id = request.form['conference_id']
        
        file = request.files['paper']
        if file.filename == '':
            flash('Please select a file', 'danger')
            return redirect(request.url)
        
        # Safe filename
        clean_name = re.sub(r'[^a-zA-Z0-9._-]', '', file.filename)
        filename = f"paper_{session['user_id']}_{clean_name}"
        file_path = os.path.join('uploads/papers', filename)
        file.save(file_path)
        
        paper = Paper(
            conference_id=conf_id,
            author_id=session['user_id'],
            title=title,
            abstract=abstract,
            keywords=keywords,
            file_path=file_path,
            status='submitted'
        )
        db.session.add(paper)
        db.session.commit()
        
        flash('Paper submitted successfully!', 'success')
        return redirect(url_for('author.my_papers'))
    
    return render_template('author/submit_paper.html', conferences=conferences)

# ====================== MY PAPERS ======================
@author_bp.route('/my_papers')
def my_papers():
    if session.get('role') != 'author':
        flash('Access Denied!', 'danger')
        return redirect(url_for('main.dashboard'))
    
    papers = Paper.query.filter_by(author_id=session['user_id']).all()
    return render_template('author/my_papers.html', papers=papers)

# ====================== UPLOAD REVISION ======================
@author_bp.route('/upload_revision/<int:paper_id>', methods=['GET', 'POST'])
def upload_revision(paper_id):
    if session.get('role') != 'author':
        flash('Access Denied!', 'danger')
        return redirect(url_for('main.dashboard'))
    
    paper = Paper.query.get_or_404(paper_id)
    
    if paper.author_id != session['user_id'] or paper.status != 'revised':
        flash('You cannot upload revision for this paper!', 'danger')
        return redirect(url_for('author.my_papers'))
    
    if request.method == 'POST':
        if 'revision_file' not in request.files:
            flash('No file selected!', 'danger')
            return redirect(request.url)
        
        file = request.files['revision_file']
        if file.filename == '':
            flash('No file selected!', 'danger')
            return redirect(request.url)
        
        filename = f"revision_{paper.id}_{file.filename}"
        file_path = os.path.join('uploads/papers', filename)
        file.save(file_path)
        
        paper.camera_ready_path = file_path
        paper.status = 'revised_submitted'
        db.session.commit()
        
        flash('Revision uploaded successfully!', 'success')
        return redirect(url_for('author.my_papers'))
    
    return render_template('author/upload_revision.html', paper=paper)

# ====================== PLAGIARISM CHECK ======================
@author_bp.route('/check_plagiarism/<int:paper_id>')
def check_plagiarism(paper_id):
    if session.get('role') != 'author':
        flash('Access Denied!', 'danger')
        return redirect(url_for('main.dashboard'))
    
    paper = Paper.query.get_or_404(paper_id)
    
    # More intelligent simulation
    text = (paper.title + " " + (paper.abstract or "")).lower()
    
    # Different categories of common academic phrases
    common_phrases = {
        'high_risk': ['artificial intelligence', 'machine learning', 'deep learning', 'neural network', 
                     'computer vision', 'natural language processing', 'data science'],
        'medium_risk': ['convolutional', 'recurrent', 'transformer', 'supervised', 'unsupervised', 
                       'reinforcement learning', 'image recognition', 'autonomous']
    }
    
    score = 30  # Base score
    
    # High risk phrases give more points
    for phrase in common_phrases['high_risk']:
        if phrase in text:
            score += 18
    
    # Medium risk phrases give fewer points
    for phrase in common_phrases['medium_risk']:
        if phrase in text:
            score += 9
    
    # Add some randomness so every paper gets slightly different score
    import random
    score += random.randint(-8, 12)
    
    # Keep score between 15 and 95
    score = max(15, min(95, score))
    
    return render_template('author/plagiarism.html', paper=paper, score=score)