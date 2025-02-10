from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image
import io
import os
import zipfile
from flask_cors import CORS
from pillow_heif import register_heif_opener

register_heif_opener()  # HEIC 파일 지원
app = Flask(__name__)
CORS(app)  # CORS 문제 해결

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB 파일 업로드 제한

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/', methods=['POST', 'GET'])
def upload():
    if 'file' not in request.files:
        print("🚨 No file key in request.files")
        return jsonify({'error': 'No file uploaded'}), 400

    files = request.files.getlist('file')
    if not files:
        print("🚨 No files selected")
        return jsonify({'error': 'No files selected'}), 400

    mode = request.form.get('mode', 'light')
    ratio = request.form.get('ratio', '1:1')
    margin = int(request.form.get('margin', 0))

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for file in files:
            try:
                image = Image.open(file.stream)
                print(f"✅ Processing file: {file.filename} (Mode: {mode}, Ratio: {ratio}, Margin: {margin})")

                # 이미지 비율 조정
                if ratio == '1:1':
                    image = Image_Convert.one2one(image, margin, mode)
                elif ratio == '5:4':
                    image = Image_Convert.four2five(image, margin, mode)
                elif ratio == '4:5':
                    image = Image_Convert.five2four(image, margin, mode)

                # 변환된 이미지 저장
                img_io = io.BytesIO()
                image.convert('RGB').save(img_io, 'JPEG')
                img_io.seek(0)

                # 압축 파일 추가
                file_name = f"converted_{file.filename}.jpg"
                zip_file.writestr(file_name, img_io.read())

            except Exception as e:
                print("🚨 Error during image processing:", e)
                return jsonify({'error': str(e)}), 500

    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='converted_images.zip')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
