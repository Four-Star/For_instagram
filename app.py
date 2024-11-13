from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image, ImageOps
import io
import os
import zipfile
import Image_Convert

app = Flask(__name__)

# 업로드된 파일을 저장할 경로
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 업로드된 파일이 저장될 폴더가 없으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/', methods=['POST', 'GET'])
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

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for file in files:
            try:
                # 파일을 Pillow 이미지로 열기
                image = Image.open(file.stream)

                # 이미지 비율 조정
                if ratio == '1:1':
                    image = Image_Convert.one2one(image, margin, mode)
                elif ratio == '5:4':
                    image = Image_Convert.four2five(image, margin, mode)
                elif ratio == '4:5':
                    image = Image_Convert.five2four(image, margin, mode)

                # 이미지를 JPEG 포맷으로 저장
                img_io = io.BytesIO()
                image.convert('RGB').save(img_io, 'JPEG')
                # image.save(img_io, 'JPEG')
                img_io.seek(0)

                # 변환된 이미지를 압축 파일에 추가
                file_name = f"converted_{file.filename}.jpg"
                zip_file.writestr(file_name, img_io.read())

            except Exception as e:
                print("Error during image processing:", e)  # 오류 메시지 출력
                return jsonify({'error': str(e)}), 500

    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='converted_images.zip')


if __name__ == '__main__':
    app.run(debug=True)
