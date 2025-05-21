from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import base64
import time

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if os.path.exists(UPLOAD_FOLDER) and not os.path.isdir(UPLOAD_FOLDER):
    os.remove(UPLOAD_FOLDER)  # 파일 삭제
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

PHOTO_FOLDER = os.path.join(UPLOAD_FOLDER, 'photo')
os.makedirs(PHOTO_FOLDER, exist_ok=True)  # PHOTO_FOLDER 디렉토리 생성

WEBCAM_FOLDER = os.path.join(UPLOAD_FOLDER, 'webcamimg')
os.makedirs(WEBCAM_FOLDER, exist_ok=True)  # WEBCAM_FOLDER 디렉토리 생성

# 허용된 파일 확장자 설정
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # 입력 데이터 가져오기
    name = request.form.get('name')
    birth = request.form.get('birth')
    phone = request.form.get('phone')
    photo = request.files.get('photo')  # 사진 파일 가져오기

    # 모든 필드가 채워졌는지 확인
    if not name or not birth or not phone:
        return jsonify({'message': '모든 항목을 입력해주세요.'}), 400

    # 사진 파일 저장
    photo_filename = "없음"  # 기본값으로 초기화
    if photo and allowed_file(photo.filename):
        photo_filename = secure_filename(photo.filename)
        photo_path = os.path.join(PHOTO_FOLDER, photo_filename)
        photo.save(photo_path)  # 파일 저장

    # addbook.txt에 데이터 저장
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'addbook.txt')
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(f"이름: {name}, 생년월일: {birth}, 전화번호: {phone}, 사진: {photo_filename}\n")

    return jsonify({'message': '주소록과 사진이 성공적으로 저장되었습니다.'}), 200

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    # 파일 가져오기
    if 'photo' not in request.files:
        return jsonify({'message': '사진 파일이 없습니다.'}), 400
    file = request.files['photo']

    # 파일 이름 확인
    if file.filename == '':
        return jsonify({'message': '파일 이름이 비어 있습니다.'}), 400

    # 파일 확장자 확인 및 저장
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(PHOTO_FOLDER, filename)  # PHOTO_FOLDER 사용
        file.save(file_path)
        return jsonify({'message': f'사진이 성공적으로 업로드되었습니다: {filename}'}), 200
    else:
        return jsonify({'message': '허용되지 않는 파일 형식입니다.'}), 400

@app.route('/capture_photo', methods=['POST'])
def capture_photo():
    # Base64로 인코딩된 이미지 데이터 가져오기
    data = request.json.get('photo_data')
    if not data:
        return jsonify({'message': '사진 데이터가 없습니다.'}), 400

    try:
        # Base64 디코딩 및 파일 저장
        photo_data = base64.b64decode(data)
        filename = f"webcam_{int(time.time())}.jpg"
        photo_path = os.path.join(WEBCAM_FOLDER, filename)  # WEBCAM_FOLDER 사용
        with open(photo_path, 'wb') as f:
            f.write(photo_data)
        return jsonify({'message': f'사진이 성공적으로 저장되었습니다: {filename}'}), 200
    except Exception as e:
        return jsonify({'message': f'사진 저장 중 오류가 발생했습니다: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
