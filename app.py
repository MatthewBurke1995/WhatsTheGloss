from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = '/static'

app = Flask(__name__)
app.secret_key = 'super_secret'

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
        chapter_numbers = request.form.get('chapter_numbers').split(' ')
        num_of_terms = int(request.form.get('num_of_terms'))
        chapters =[['a','b','c','d'],['x','y','z'],['e','f','g','h']]
        chapters = list(important_words_per_chapter(pdf_file, num_of_terms))
        print(num_of_terms)
        print(chapter_numbers)
        return render_template('index.html', chapters=chapters)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    flaskapp.run(debug=True)





import PyPDF2
#pdfFileObj = open('biology.pdf', 'rb')
#pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer
stop_words = stopwords.words('english')




def tokenize(text):
    """Helper tokenize function for making each word in the pdf a recognizable english word"""
    text=text.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    return [w for w in tokens if w not in stop_words and not w.isdigit() ]



def important_words_per_chapter(pdf_file, num_of_terms):
    #pdfFileObj = open(pdf_file, 'rb')

    pdfReader = PyPDF2.PdfFileReader(pdf_file)
    full_text=[]
    for i in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(i)
        full_text.append(pageObj.extractText())

    full_text = ' '.join(full_text)
    chapter_text = full_text.split('CHAPTER')[1:]


    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words=stop_words)
    tfs = tfidf.fit_transform(chapter_text)
    feature_names = tfidf.get_feature_names()

    chapters_left=len(chapter_text)
    currentchapter=0
    while currentchapter < len(chapter_text):

        response = tfidf.transform([chapter_text[currentchapter]])

        yield([feature_names[col] for col in
           sorted(response.nonzero()[1],key= lambda col:response[0, col], reverse=True)[:num_of_terms]])
        currentchapter+=1


