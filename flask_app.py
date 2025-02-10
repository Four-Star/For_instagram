from flask import Flask, render_template, request, jsonify, send_file, Response
from PIL import Image
import io
import os
import zipfile
import Image_Convert

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

    mode = request.form.get('mode', 'light')
    ratio = request.form.get('ratio', '1:1')
    margin = int(request.form.get('margin', 0))

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for file in files:
            try:
                image = Image.open(file.stream)

                if ratio == '1:1':
                    image = Image_Convert.one2one(image, margin, mode)
                elif ratio == '5:4':
                    image = Image_Convert.four2five(image, margin, mode)
                elif ratio == '4:5':
                    image = Image_Convert.five2four(image, margin, mode)

                img_io = io.BytesIO()
                image.convert('RGB').save(img_io, 'JPEG')
                img_io.seek(0)

                file_name = f"converted_{file.filename}.jpg"
                zip_file.writestr(file_name, img_io.read())

            except Exception as e:
                print("Error during image processing:", e)
                return jsonify({'error': str(e)}), 500

    zip_buffer.seek(0)

    # 👇 **추가된 부분 (헤더 설정)**
    response = Response(zip_buffer.getvalue(), mimetype='application/zip')
    response.headers['Content-Disposition'] = 'attachment; filename=converted_images.zip'
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Pragma'] = 'no-cache'

    return response

if __name__ == '__main__':
    app.run(debug=True)
