from flask import Flask, render_template, request, jsonify, send_file, Response
from PIL import Image
import io
import os
import zipfile
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

    zip_id = str(uuid.uuid4())  # 고유한 파일명 생성
    zip_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{zip_id}.zip")

    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for file in files:
            try:
                # 파일을 Pillow 이미지로 열기
                image = Image.open(file.stream)

                # 이미지 비율 조정 (예제용, 변환 함수 직접 구현 필요)
                image = image.convert('RGB')  # 기본 RGB 변환 적용

                # 이미지를 메모리에서 저장
                img_io = io.BytesIO()
                image.save(img_io, 'JPEG')
                img_io.seek(0)

                # 변환된 이미지를 압축 파일에 추가
                file_name = f"converted_{file.filename}.jpg"
                zip_file.writestr(file_name, img_io.read())

            except Exception as e:
                return jsonify({'error': str(e)}), 500

    # 변환된 파일 다운로드 URL 반환
    return jsonify({'download_url': f'/download/{zip_id}'})

@app.route('/download/<zip_id>')
def download(zip_id):
    zip_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{zip_id}.zip")

    if not os.path.exists(zip_path):
        return jsonify({'error': 'File not found'}), 404

    # 파일 다운로드를 위한 Content-Disposition 헤더 설정
    response = Response(open(zip_path, 'rb').read(), mimetype='application/zip')
    response.headers["Content-Disposition"] = f"attachment; filename=converted_images.zip"
    return response

if __name__ == '__main__':
    app.run(debug=True)
