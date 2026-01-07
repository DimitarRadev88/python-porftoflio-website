from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.validators import Length, Email
from flask_bootstrap import Bootstrap5
from wtforms import StringField, TextAreaField, SubmitField
import smtplib
from dotenv import load_dotenv
import os

class MessageForm(FlaskForm):
    email = StringField('Email Address',validators=[Email()])
    message = TextAreaField('Message',validators=[Length(min=10, max=1000)])
    submit = SubmitField("Send")

load_dotenv("secrets.env")

SECRET_KEY = os.getenv("SECRET_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
SMTP = os.getenv("SMTP")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
bootstrap = Bootstrap5(app)

def send_message(text, address):
    smtp = smtplib.SMTP(SMTP)
    smtp.starttls()
    smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
    smtp.sendmail(from_addr=SENDER_EMAIL,
                  to_addrs=SENDER_EMAIL,
                  msg=f"Subject: New message from: {address}\n\n{text}")
    smtp.quit()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = MessageForm()
    if form.validate_on_submit():
        send_message(form.message.data, form.email.data)
        return redirect(url_for("contact"))

    return render_template("contact.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)