# app.py
import os
from email_service import send_booking_emails
from flask import Flask, render_template, redirect, url_for, flash
from dotenv import load_dotenv
from models import db, Booking
from forms import BookingForm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///leadops.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SMTP_HOST"] = os.getenv("SMTP_HOST")
app.config["SMTP_PORT"] = int(os.getenv("SMTP_PORT", "465"))
app.config["SMTP_USER"] = os.getenv("SMTP_USER")
app.config["SMTP_PASSWORD"] = os.getenv("SMTP_PASSWORD")
app.config["MAIL_FROM"] = os.getenv("MAIL_FROM")
app.config["BUSINESS_EMAIL"] = os.getenv("BUSINESS_EMAIL")
app.config["APP_BASE_URL"] = os.getenv("APP_BASE_URL", "")

db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/book", methods=["GET", "POST"])
def book():
    form = BookingForm()

    if form.validate_on_submit():
        booking = Booking(
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            service=form.service.data,
            preferred_date=form.preferred_date.data,
            preferred_time=form.preferred_time.data,
            notes=form.notes.data,
        )
        db.session.add(booking)
        db.session.commit()

        try:
            send_booking_emails(booking)
        except Exception as e:
            app.logger.exception("Error sending booking emails: %s", e)

        flash("Booking request received. We’ll confirm shortly.", "success")
        return redirect(url_for("booking_success"))

    return render_template("book.html", form=form)

@app.route("/book/success")
def booking_success():
    return render_template("booking_success.html")

@app.route("/features/voice-receptionist")
def voice_receptionist():
    return render_template("feature_voice.html")

@app.route("/features/automated-confirmations")
def automated_confirmations():
    return render_template("feature_confirmations.html")

@app.route("/features/schedule-optimization")
def schedule_optimization():
    return render_template("feature_schedule.html")

@app.route("/features/integrations")
def integrations():
    return render_template("feature_integrations.html")

@app.route("/features/outreach")
def outreach():
    return render_template("feature_outreach.html")

@app.route("/features/client-management")
def client_management():
    return render_template("feature_client_management.html")
