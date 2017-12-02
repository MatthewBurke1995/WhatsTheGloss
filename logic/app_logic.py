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



def important_words_per_chapter(pdf_file, chapter_numbers):
    num_of_terms=20

    pdfReader = PyPDF2.PdfFileReader(pdf_file)
    chapter_text=[]
    previous_starting_page=0
    for index,starting_page in enumerate(chapter_numbers):
        single_chapter =[]

        for j in range(previous_starting_page, starting_page):
            pageObj = pdfReader.getPage(j)
            single_chapter.append(pageObj.extractText())

        previous_starting_page = starting_page
        chapter_text.append(' '.join(single_chapter))


    chapter_text = chapter_text[1:]
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
