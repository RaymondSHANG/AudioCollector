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
from application.models import AudioRecord
from application import db
import random
from datetime import datetime

audioCollect_bp = Blueprint(
    'audioCollect_bp',
    __name__,
    url_prefix='/audioCollect',
    template_folder='templates'
)

@audioCollect_bp.route('/myAudio', methods=['GET'])
@login_required
def myAudio():
    try:
        audiohistory = db.session.query(
            News.id,  # ID from AudioRecord
            News.title,  # Title from News
            News.level,  # Level from News
            AudioRecord.record_date,  # Record date from AudioRecord
            AudioRecord.duration,
            AudioRecord.score 
        ).join(News, AudioRecord.news_id == News.id  # Joining AudioRecord with News on news_id
        ).filter(AudioRecord.patient_id == current_user.id  # Filtering by user.id not patient_id
        ).order_by(AudioRecord.record_date.desc()  # Assuming the date field is named 'record_date'
        ).limit(10).all()

        #nåews_select = News.query.order_by(News.record_date.desc()).limit(10).all()
        if not audiohistory:
            flash('There is no audio recordings in the database! Record now!')
            return redirect(url_for('audioCollect_bp.audioCollect'))
        
        return render_template('audioHistory.html',  audiohistory = audiohistory)
    except Exception as e:
        current_app.logger.error(f"Error accessing audio history: {e}")
        flash('Error accessing audio history.')
        #return redirect(url_for('audioCollect_bp.audioCollect'))

@audioCollect_bp.route('/audioCollect', methods=['GET'])
@login_required
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
@login_required
def upload():
    if 'audio' not in request.files:
        return 'No file part'
    audio = request.files['audio']
    if audio.filename == '':
        return 'No selected file'
    datetime_postfix = datetime.now().strftime("_%Y%m%d_%H%M%S")
    base_filename = request.form.get('filename', 'recording')  # Default to 'recording' if not provided
    flash(base_filename)
    # Create the complete filename with datetime postfix
    filename = f"record_{current_user.patient_id}_NewsID{base_filename}_{datetime_postfix}.wav"
    
    if not filename:
        filename = 'recording'
    
    duration = request.form.get('duration')  # Get the duration from the form

    if audio:
        # Save the audio file with the specified filename
        audio_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        audio.save(audio_path)
        # Update database:
        news_id = int(base_filename)
        news_record = AudioRecord(patient_id=current_user.id,
                         news_id=news_id,
                         record_date=datetime.now(),
                         file_dir=filename,
                         duration=duration
                         )
                    
        db.session.add(news_record)
        db.session.commit()

        flash("File uploaded successfully")
        return redirect(url_for('audioCollect_bp.myAudio'))
    return redirect(url_for('audioCollect_bp.myAudio'))