# Import necessary modules and classes from Flask and other packages
from flask import Blueprint, render_template, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from flask import *
from flask_mail import Message
from .__init__ import mail
from . import scheduler
from datetime import datetime
from datetime import timedelta
import logging
from apscheduler.schedulers.background import BackgroundScheduler

# Create a Blueprint named 'views'
views = Blueprint('views', __name__)

# Define a route for the home page, accessible only to logged-in users
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # Set up logging and log the current date
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(datetime.now().date())
    
    # Handle form submission on the home page
    with current_app.app_context():
        if request.method == 'POST': 
            note = request.form.get('note')
            scheduled_date = request.form.get('date')

            # Validate and handle note and scheduled_date inputs
            if len(note) < 1:
                flash('Note is too short!', category='error') 
            elif not scheduled_date:
                flash('You need to include a date!', category='error')
            else:
                # Create a new note and schedule an email
                new_note = Note(data=note, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                schedule_email(current_user.email, note, scheduled_date, new_note.id, current_app._get_current_object())
        
    # Render the home.html template and pass the current user
    return render_template("home.html", user=current_user)

# Schedule an email to be sent at a specified date
def schedule_email(email, note, scheduled_date, noteId, app):
    with app.app_context():
        scheduled_datetime = datetime.strptime(scheduled_date, "%Y-%m-%d")
        scheduled_date_only = scheduled_datetime.date()
        if scheduled_date_only >= datetime.now().date():
            extended_run_date = scheduled_datetime + timedelta(minutes=123) 
            scheduler.add_job(
                send_scheduled_email,
                'date',
                args=[email, note, noteId, app],
                run_date=extended_run_date
            )
            flash('Email scheduled!', category='success')
        else:
            flash('Scheduled date must be in the future!', category='error')

# Send a scheduled email and delete the corresponding note
def send_scheduled_email(email, body, noteId, app):
    with app.app_context():
        msg = Message(subject="IMPORTANT REMINDER", body=body, sender='reminder.noreply987@gmail.com')
        msg.add_recipient(email)
        mail.send(msg)

        # Delete the note after sending the email
        with app.app_context():
            note = Note.query.get(noteId)
            if note:
                db.session.delete(note)
                db.session.commit()

# Define a route to delete a note
@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})