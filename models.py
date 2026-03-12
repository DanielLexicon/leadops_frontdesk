from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), nullable=False)
    phone = db.Column(db.String(60))
    service = db.Column(db.String(120), nullable=False)
    preferred_date = db.Column(db.String(40), nullable=False)
    preferred_time = db.Column(db.String(40), nullable=False)
    notes = db.Column(db.Text)
    status = db.Column(db.String(30), default="pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
