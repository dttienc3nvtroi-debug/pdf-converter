from flask import Flask, request, send_file
from flask_cors import CORS
from pdf2docx import Converter
import os
import tempfile

app = Flask(__name__)
CORS(app) # Cho phép Web từ bên ngoài gửi request tới

@app.route('/', methods=['GET'])
def home():
    return "Server PDF to Word Online đang hoạt động!"

@app.route('/convert', methods=['POST'])
def convert_pdf_to_docx():
    if 'file' not in request.files:
        return {"error": "Không tìm thấy file!"}, 400
    
    file = request.files['file']
    temp_dir = tempfile.gettempdir()
    pdf_path = os.path.join(temp_dir, file.filename)
    docx_path = os.path.join(temp_dir, file.filename.replace('.pdf', '.docx'))
    
    file.save(pdf_path)
    
    try:
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)
        cv.close()
        return send_file(docx_path, as_attachment=True)
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        if os.path.exists(pdf_path): os.remove(pdf_path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)