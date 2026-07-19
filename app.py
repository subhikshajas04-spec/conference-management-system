from flask import Flask, send_from_directory
from config import Config
from models import db, User
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.config.from_object(Config)

# CRITICAL: Add this line - Without it login/session will NOT work
app.secret_key = 'confhub-super-secret-key-2026'   # Change this in production

# Create folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('instance', exist_ok=True)

db.init_app(app)

# Create database + Default Admin
with app.app_context():
    
    db.create_all()
    
    if not User.query.filter_by(email='admin@cms.com').first():
        admin = User(
            name='Super Admin',
            email='admin@cms.com',
            password=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Default Admin created: admin@cms.com / admin123")
    
    print("✅ Database created successfully!")
    
# ====================== REGISTER ALL BLUEPRINTS ======================
from routes.auth import auth_bp
from routes.main import main_bp
from routes.author import author_bp
from routes.organizer import organizer_bp
from routes.reviewer import reviewer_bp
from routes.attendee import attendee_bp
from routes.admin import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(author_bp)
app.register_blueprint(organizer_bp)
app.register_blueprint(reviewer_bp)
app.register_blueprint(attendee_bp)
app.register_blueprint(admin_bp)

print("✅ All blueprints registered successfully!")

# ====================== SERVE UPLOADED FILES ======================
@app.route('/uploads/papers/<path:filename>')
def uploaded_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        return "File not found", 404

print("✅ File serving route added!")
print("✅ Server started at: http://127.0.0.1:5000")

if __name__ == '__main__':
    app.run(debug=True)