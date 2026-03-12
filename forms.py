from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

class BookingForm(FlaskForm):
    full_name = StringField("Full name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    phone = StringField("Phone (optional)")
    service = SelectField(
        "Service",
        choices=[
            ("Haircut", "Haircut"),
            ("Color / Highlights", "Color / Highlights"),
            ("Beard / Shave", "Beard / Shave"),
            ("Facial / Skin Care", "Facial / Skin Care"),
            ("Massage", "Massage"),
            ("Consultation", "Consultation"),
        ],
        validators=[DataRequired()],
    )
    preferred_date = StringField("Preferred date", validators=[DataRequired()])
    preferred_time = StringField("Preferred time", validators=[DataRequired()])
    notes = TextAreaField("Notes (optional)")
    submit = SubmitField("Request Booking")
