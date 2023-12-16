from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.http import JsonResponse
from joblib import dump, load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from mpstemmer import MPStemmer
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import nltk
import re
import pickle
import pandas
from functools import lru_cache
nltk.download('punkt')


# Load the model and X_train once
def preprocessing(sentence):
    stop_factory = StopWordRemoverFactory()
    stop_words_list = stop_factory.get_stop_words()
    stop_words_set  = set(stop_words_list)
    result = []

    # Regex for tokenization
    tokenizer_pattern = r'\w+'

    # For stemming and lemmatization
    stemmer = MPStemmer()

    # Proses untuk tokenization dan lemmatization
    # dan membuang stopword
    tokens =  re.findall(tokenizer_pattern, sentence)
    for token in tokens:
        token = stemmer.stem(token).lower()
        if token != '' and token != None and token not in stop_words_set:
            result.append(token)
    return result

loaded_model = pickle.load(open('best_svc.pickle', 'rb'))
X_train = pickle.load(open('X_train.pickle', 'rb'))
loaded_feature_extraction = TfidfVectorizer(tokenizer=preprocessing)
loaded_feature_extraction.fit_transform(X_train)

@lru_cache(maxsize=None)  
def get_transformed_data(text):
    text_non = [text]
    test = loaded_feature_extraction.transform(text_non)
    res_ = loaded_model.predict(test)
    return classify(res_)

def home(request):
	return render(request, 'base/index.html')

def spam_classification(request):
	return render(request, 'base/spam_class.html')

def classify(res):
    if res == 1:
        return 'This message is SPAM'
    return 'This message is not SPAM'

def classify_sms(request):
    result = None

    if request.method == 'POST':
        sms_text = request.POST.get('sms_text')
        if sms_text:
            result = get_transformed_data(sms_text)
            if request.is_ajax():
                return JsonResponse({'result': result})

    return JsonResponse({'result': 'Invalid request'})

def sendEmail(request):

	if request.method == 'POST':

		template = render_to_string('base/email_template.html', {
			'name':request.POST['name'],
			'email':request.POST['email'],
			'message':request.POST['message'],
			})

		email = EmailMessage(
			request.POST['subject'],
			template,
			settings.EMAIL_HOST_USER,
			['hizkia.sebastian@ui.ac.id']
			)

		email.fail_silently=False
		email.send()

	return render(request, 'base/email_sent.html')