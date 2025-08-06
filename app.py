from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import tempfile
import shutil

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'md', 'txt', 'yml', 'yaml', 'json'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({'error': 'Keine Dateien ausgewählt'}), 400
    
    files = request.files.getlist('files')
    config_file = request.files.get('config')
    
    if not files:
        return jsonify({'error': 'Keine Dateien ausgewählt'}), 400
    
    uploaded_files = []
    
    # Save uploaded markdown files
    for file in files:
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            uploaded_files.append(filepath)
    
    # Save config file if provided
    config_path = None
    if config_file and config_file.filename and allowed_file(config_file.filename):
        config_filename = secure_filename(config_file.filename)
        config_path = os.path.join(UPLOAD_FOLDER, config_filename)
        config_file.save(config_path)
    
    return jsonify({
        'message': f'{len(uploaded_files)} Dateien erfolgreich hochgeladen',
        'files': uploaded_files,
        'config': config_path
    })

@app.route('/merge', methods=['POST'])
def merge_markdown():
    # This will be implemented in the next step
    return jsonify({'message': 'Merge-Funktionalität wird implementiert'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)