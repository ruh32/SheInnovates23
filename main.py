from flask import Flask, flash, render_template, redirect, request
from pathlib import Path
from PyPDF2 import PdfMerger
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config['SECRET_KEY'] = 'julianneiscool'
app.config['UPLOAD_FOLDER'] = 'UPLOAD_FOLDER'

@app.route('/', methods=['GET', 'POST'])
def home():
   return render_template('index.html')
@app.route('/upload.html', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files.getlist("upload")
        for file in f:
            if file.filename == '':
                #flash("No selected file")
                return redirect(request.url)
            if file.filename != '':
                filename = (secure_filename(file.filename))
                save_path = Path('UPLOAD_FOLDER', filename)
                file.save(save_path)
        merge_pdfs()
        return render_template('display.html')
    #new_file = convert_to_schedule(save_path)
    return render_template('upload.html')

def convert_to_schedule(save_path):
   #KAVINS CODE HERE
   return 0

def image_to_text():
    return 0

def merge_pdfs():
    merger = PdfMerger()
    for filename in os.listdir('UPLOAD_FOLDER'):
        f = os.path.join('UPLOAD_FOLDER', filename)
        merger.append(f)
    merger.write("templates/result.pdf")
    merger.close()

if __name__ == '__main__':
   app.run()
