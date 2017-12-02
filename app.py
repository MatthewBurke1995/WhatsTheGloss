from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = '/static'
app = Flask(__name__)
app.secret_key = 'super_secret'

import logic.app_logic as logic

""" You're not gonna need it

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['pdf'])
def allowed_file(filename):
    return '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
"""



@app.route('/', methods=['GET','POST'])
def main_app():

    if request.method == 'POST':
        if 'file' not in request.files:
            print('no file')
            return redirect(url_for('main_app'))
        pdf_file = request.files['file']


        chapter_numbers = request.form.get('chapter_numbers', None)
        if chapter_numbers:
            chapter_numbers = [int(i) for i in chapter_numbers.split(' ')]
            chapters = list(logic.important_words_per_chapter(pdf_file,  chapter_numbers=chapter_numbers))


        chapter_phrase = request.form.get('chapter_phrase', None)
        if chapter_phrase and not chapter_numbers:
            chapters = list(logic.important_words_per_chapter(pdf_file,  chapter_phrase=chapter_phrase))





        return render_template('index.html', chapters=chapters)


    else:
        return render_template('index.html')

if __name__ == '__main__':
    flaskapp.run(debug=True)

