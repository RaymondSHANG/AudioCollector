from flask import render_template, Blueprint, session, flash, redirect, url_for, request,current_app
from flask_login import current_user, login_required
from fhirclient.models.patient import Patient
import os
from contextlib import suppress
from application.fhir.connect import connector
from application.fhir.search import ResourceFinder
#from application.oauth.utils import oauth_required
from application.fhir.connect import smart
from application.models import News
from application import db
import random

audioCollect_bp = Blueprint(
    'audioCollect_bp',
    __name__,
    url_prefix='/audioCollect',
    template_folder='templates'
)


@audioCollect_bp.route('/', methods=['GET'])
#@login_required
def audioCollect():
    news_select = News.query.order_by(News.pub_date.desc()).limit(10).all()
    if not news_select:
        flash('There is no news in the database! Add news first!')
        return redirect(url_for('news_bp.addNews'))
    # News.query.all()
    oneNews = random.choice(news_select)
    
    patient = Patient.read(current_user.patient_id, smart.server)
    flash(f"Welcome, {patient.name[0].given[0]}")
    ## To do:
       ## Fetch a news and send to index
    return render_template('audioCollect.html', patient=patient,smart=smart, news = oneNews)

@audioCollect_bp.route('/upload', methods=['POST'])
#@login_required
def upload():
    if 'audio' not in request.files:
        return 'No file part'
    audio = request.files['audio']
    if audio.filename == '':
        return 'No selected file'
    filename = request.form.get('filename')  # Get the filename from the form
    filename = "record_"+str(current_user.patient_id)
    if not filename:
        filename = 'recording'
    
    duration = request.form.get('duration')  # Get the duration from the form

    if audio:
        # Save the audio file with the specified filename
        audio_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename + '.wav')
        audio.save(audio_path)
        flash("File uploaded successfully")
        return redirect(url_for('audioCollect_bp.audioCollect'))
    return redirect(url_for('audioCollect_bp.audioCollect'))