from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = '/static'
application = Flask(__name__)
application.secret_key = 'super_secret'

import re
import logic.app_logic as logic


@application.route('/')
def main_app():
    return render_template('index.html')

@application.route('/walkthrough.html')
def walkthrough():
    return render_template('walkthrough.html')

@application.route('/explanation.html')
def insides():
    return render_template('explanation.html')


@application.route('/glossary.html', methods=['GET','POST'])
def show_glossary():
    if request.method == 'POST':
        file_ = request.files['file']
        chapter_numbers = request.form.get('chapter_numbers', None)
        chapter_phrase = request.form.get('chapter_phrase', None)

        if file_.filename.endswith('pdf'):
            pdf_file = file_

            if chapter_numbers:
                chapter_numbers = [int(i) for i in re.split('\D+', chapter_numbers)]
                chapter_text = logic.get_chapter_text_pdf(pdf_file, chapter_numbers = chapter_numbers)
                glossary = logic.get_glossary(chapter_text)

            elif chapter_phrase:
                chapter_text = logic.get_chapter_text_pdf(pdf_file, chapter_phrase=chapter_phrase)
                glossary = logic.get_glossary(chapter_text)


        elif file_.filename.endswith('txt'):
            txt_file = file_

            if chapter_phrase:
                chapter_text = logic.get_chapter_text_txt(txt_file, chapter_phrase = chapter_phrase)
                glossary = logic.get_glossary(chapter_text)

            elif chapter_numbers:
                return render_template('errors.html', error="Text files can't use page numbers, try using a phrase to seperate chapters")

        glossary = [logic.unique_stems(chapter) for chapter in glossary]
        return render_template('glossary.html', glossary=glossary)

    else:
        return render_template('index.html')


@application.errorhandler(500)
def page_not_found(e):
    return render_template('errors.html', error="There was an error processing the file")

@application.errorhandler(404)
def page_not_found(e):
    return render_template('errors.html', error="It looks like that page doesn't exist")

if __name__ == '__main__':
    flaskapp.run(debug=True)

