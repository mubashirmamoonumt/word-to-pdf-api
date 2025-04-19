from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import os
from docx2pdf import convert

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "Word to PDF API is running."

@app.route('/convert', methods=['POST'])
def convert_to_pdf():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Convert DOCX to PDF
    try:
        convert(filepath)
        pdf_path = filepath.replace('.docx', '.pdf')
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        return str(e), 500
