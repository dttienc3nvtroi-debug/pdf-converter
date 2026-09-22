import os
from flask import Flask, request, send_file
from flask_cors import CORS
from pdf2docx import Converter

app = Flask(__name__)
CORS(app)  # Cho phép mọi trang web/file HTML gửi yêu cầu đến backend

@app.route('/')
def home():
    return "Server PDF to Word Online đang hoạt động!"

@app.route('/convert', methods=['POST'])
def convert_pdf_to_docx():
    if 'file' not in request.files:
        return "Không tìm thấy file tải lên", 400
    
    file = request.files['file']
    if file.filename == '':
        return "Chưa chọn file", 400

    pdf_path = os.path.join('/tmp', file.filename)
    docx_filename = os.path.splitext(file.filename)[0] + '.docx'
    docx_path = os.path.join('/tmp', docx_filename)

    file.save(pdf_path)

    try:
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)
        cv.close()

        return send_file(docx_path, as_attachment=True, download_name=docx_filename)
    except Exception as e:
        return str(e), 500
    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
