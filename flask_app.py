from flask import Flask, render_template, request, jsonify, send_file, Response
from PIL import Image
import io
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    files = request.files.getlist('file')
    if not files:
        return jsonify({'error': 'No files selected'}), 400

    download_links = []

    for file in files:
        try:
            image = Image.open(file.stream)
            image = image.convert('RGB')

            file_id = str(uuid.uuid4())
            file_name = f"converted_{file_id}.jpg"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            image.save(file_path, 'JPEG')

            download_links.append(f'/download/{file_name}')

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'download_urls': download_links})

@app.route('/download/<file_name>')
def download(file_name):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    # 직접 Content-Disposition 헤더 설정
    response = Response(open(file_path, 'rb').read())
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response

if __name__ == '__main__':
    app.run(debug=True)
