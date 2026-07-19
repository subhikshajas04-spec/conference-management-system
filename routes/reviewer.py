from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Paper, PaperAssignment, Review

reviewer_bp = Blueprint('reviewer', __name__)

@reviewer_bp.route('/my_assignments')
def my_assignments():
    if session.get('role') != 'reviewer':
        flash('Access Denied!', 'danger')
        return redirect(url_for('main.dashboard'))
    
    assignments = PaperAssignment.query.filter_by(reviewer_id=session['user_id']).all()
    papers = [Paper.query.get(a.paper_id) for a in assignments if Paper.query.get(a.paper_id)]
    
    return render_template('reviewer/my_assignments.html', papers=papers)

@reviewer_bp.route('/review_paper/<int:paper_id>', methods=['GET', 'POST'])
def review_paper(paper_id):
    if session.get('role') != 'reviewer':
        flash('Access Denied!', 'danger')
        return redirect(url_for('main.dashboard'))
    
    paper = Paper.query.get_or_404(paper_id)
    
    if request.method == 'POST':
        review = Review(
            paper_id=paper_id,
            reviewer_id=session['user_id'],
            score=int(request.form['score']),
            comments=request.form['comments'],
            recommendation=request.form['recommendation']
        )
        db.session.add(review)
        db.session.commit()
        
        paper.status = 'under_review'
        db.session.commit()
        
        flash('Review submitted successfully!', 'success')
        return redirect(url_for('reviewer.my_assignments'))
    
    return render_template('reviewer/review_paper.html', paper=paper)