from flask import Flask, request, send_from_directory,render_template, flash
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the 'uploads' directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio' not in request.files:
        return 'No file part'
    audio = request.files['audio']
    if audio.filename == '':
        return 'No selected file'
    filename = request.form.get('filename')  # Get the filename from the form

    if not filename:
        filename = 'recording'

    duration = request.form.get('duration')  # Get the duration from the form

    if audio:
        # Save the audio file with the specified filename
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + '.wav')
        audio.save(audio_path)
        flash("File uploaded successfully")
        return 'File uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)