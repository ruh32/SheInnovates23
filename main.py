from flask import Flask, render_template, redirect, request
from pathlib import Path
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
            if file.filename != '':
                filename = (secure_filename(file.filename))
                save_path = Path('UPLOAD_FOLDER', filename)
                file.save(save_path)
        return "Files uploaded success fully"
      #new_file = convert_to_schedule(save_path)
    #REPLACE the return ^^^ WITH: return render_template('download.html', file = new_file)
    return render_template('upload.html')

def convert_to_schedule(save_path):
   #KAVINS CODE HERE
   return 0

if __name__ == '__main__':
   app.run()
