from flask import Flask, render_template, request, jsonify, send_file, Response
from PIL import Image
import io
import os
import uuid

app = Flask(__name__)

# 업로드된 파일을 저장할 경로
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 업로드 폴더가 없으면 생성
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

    # 옵션 값 가져오기
    mode = request.form.get('mode', 'light')
    ratio = request.form.get('ratio', '1:1')
    margin = int(request.form.get('margin', 0))

    download_links = []  # 변환된 개별 파일의 다운로드 링크 리스트

    for file in files:
        try:
            # 파일을 Pillow 이미지로 열기
            image = Image.open(file.stream)

            # 이미지 비율 조정 (예제용, 변환 함수 직접 구현 필요)
            image = image.convert('RGB')  # 기본 RGB 변환 적용

            # 변환된 이미지를 개별 파일로 저장
            file_id = str(uuid.uuid4())  # 고유한 파일명 생성
            file_name = f"converted_{file_id}.jpg"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            image.save(file_path, 'JPEG')

            # 다운로드 링크 추가
            download_links.append(f'/download/{file_name}')

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # 변환된 개별 이미지 다운로드 URL 반환
    return jsonify({'download_urls': download_links})

@app.route('/download/<file_name>')
def download(file_name):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    # 개별 파일 다운로드
    return send_file(file_path, mimetype='image/jpeg', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
