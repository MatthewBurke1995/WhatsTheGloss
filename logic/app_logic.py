import PyPDF2
#pdfFileObj = open('biology.pdf', 'rb')
#pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer
from nltk.stem import *
import itertools

stop_words = 'i me my myself we our ours ourselves you your yours yourself yourselves he him his himself she her hers herself it its itself they them their theirs themselves what which who whom this that these those am is are was were be been being have has had having do does did doing a an the and but if or because as until while of at by for with about against between into through during before after above below to from up down in out on off over under again further then once here there when where why how all any both each few more most other some such no nor not only own same so than too very s t can will just don should now d ll m o re ve y ain aren couldn didn doesn hadn hasn haven isn ma mightn mustn needn shan shouldn wasn weren won wouldn'.split(' ')


def unique_stems(list_of_words, stemmer=SnowballStemmer('english')):
    stems = [stemmer.stem(word) for word in list_of_words]
    stem_word_dic = dict(itertools.zip_longest(stems, list_of_words))
    return [stem_word_dic.get(word,word) for word in set(stems)]




def tokenize(text):
    """Helper tokenize function for making each word in the pdf a recognizable english word"""
    text=text.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    return [w for w in tokens if w not in stop_words and w.isalpha()]



def important_words_per_chapter(pdf_file, chapter_numbers=None, chapter_phrase=None):
    """Input of pdf file, chapter """
    num_of_terms=20
    pdfReader = PyPDF2.PdfFileReader(pdf_file, strict=False)

    if chapter_numbers:
        chapter_text = get_chapters_from_nums(pdfReader, chapter_numbers)

    if chapter_phrase:
        chapter_text = get_chapters_from_phrase(pdfReader, chapter_phrase)

    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words=stop_words)
    tfs = tfidf.fit_transform(chapter_text) #Not just assigning variable this line changes state
    feature_names = tfidf.get_feature_names()

    currentchapter=0
    while currentchapter < len(chapter_text):
        response = tfidf.transform([chapter_text[currentchapter]])

        yield([feature_names[col] for col in sorted(response.nonzero()[1],
		key= lambda col:response[0, col], reverse=True)[:num_of_terms]])
        currentchapter+=1






def get_chapters_from_nums(pdfReader,chapter_numbers):
    """ """
    chapter_text=[]
    previous_starting_page=0
    for index,starting_page in enumerate(chapter_numbers):
        single_chapter =[]

        for j in range(previous_starting_page, starting_page):
            pageObj = pdfReader.getPage(j)
            single_chapter.append(pageObj.extractText())

        previous_starting_page = starting_page
        chapter_text.append(' '.join(single_chapter))

    return chapter_text[1:] #return chapters without prologue 



import re
def get_chapters_from_phrase(pdfReader, chapter_phrase):
    full_text=[]
    for i in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(i)
        full_text.append(pageObj.extractText())

    full_text = ' '.join(full_text)
    chapter_text = re.split(chapter_phrase, full_text)
    return chapter_text[1:] #return chapters without prologue

