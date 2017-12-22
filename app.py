from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = '/static'
app = Flask(__name__)
app.secret_key = 'super_secret'
import re
import logic.app_logic as logic


@app.route('/')
def main_app():
    return render_template('index.html')

@app.route('/glossary.html', methods=['GET','POST'])
def show_glossary():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('no file')
            return "Error: no file was attached"
            #return redirect(url_for('main_app'))
        pdf_file = request.files['file']


        chapter_numbers = request.form.get('chapter_numbers', None)
        if chapter_numbers:
            chapter_numbers = [int(i) for i in re.split('\D+', chapter_numbers)]
            chapters = list(logic.important_words_per_chapter(pdf_file,  chapter_numbers=chapter_numbers))


        chapter_phrase = request.form.get('chapter_phrase', None)
        if chapter_phrase and not chapter_numbers:
            chapters = list(logic.important_words_per_chapter(pdf_file,  chapter_phrase=chapter_phrase))

        chapters = [logic.unique_stems(chapter) for chapter in chapters]
        return render_template('glossary.html', chapters=chapters)


    else:
        return render_template('index.html')


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500error.html')


if __name__ == '__main__':
    flaskapp.run(debug=True)

