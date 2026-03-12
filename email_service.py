# email_service.py
import smtplib
from datetime import datetime
from email.message import EmailMessage
from flask import current_app, render_template


def _format_date(raw):
    if not raw:
        return raw
    for fmt in ("%d%m%y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(raw, fmt).strftime("%d/%m/%Y")
        except ValueError:
            continue
    return raw


def _send_email(to_email, subject, text_body, html_body=None):
    smtp_host = current_app.config.get("SMTP_HOST")
    smtp_port = int(current_app.config.get("SMTP_PORT", 465))
    smtp_user = current_app.config.get("SMTP_USER")
    smtp_pass = current_app.config.get("SMTP_PASSWORD")
    mail_from = current_app.config.get("MAIL_FROM") or smtp_user

    if not smtp_host or not smtp_user or not smtp_pass:
        raise RuntimeError("Missing SMTP config: SMTP_HOST/SMTP_USER/SMTP_PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = mail_from
    msg["To"] = to_email
    msg.set_content(text_body)
    if html_body:
        msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30) as server:
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)


def send_booking_emails(booking):
    base_url = current_app.config.get("APP_BASE_URL", "")
    business_email = current_app.config.get("BUSINESS_EMAIL")
    pretty_date = _format_date(booking.preferred_date)

    client_subject = "Booking request received"
    client_text = f"""Hi {booking.full_name},

We received your booking request for {booking.service}.
Preferred date: {pretty_date}
Preferred time: {booking.preferred_time}

We’ll confirm shortly.

LeadOps Front Desk
"""
    client_html = render_template(
        "emails/booking_confirmation.html",
        booking=booking,
        pretty_date=pretty_date,
        base_url=base_url,
    )
    _send_email(booking.email, client_subject, client_text, client_html)

    if business_email:
        biz_subject = f"New booking request: {booking.full_name}"
        biz_text = f"""New booking request:

Name: {booking.full_name}
Email: {booking.email}
Phone: {booking.phone}
Service: {booking.service}
Preferred date: {pretty_date}
Preferred time: {booking.preferred_time}
Notes: {booking.notes}

LeadOps Front Desk
"""
        biz_html = render_template(
            "emails/booking_notification.html",
            booking=booking,
            pretty_date=pretty_date,
            base_url=base_url,
        )
        _send_email(business_email, biz_subject, biz_text, biz_html)
