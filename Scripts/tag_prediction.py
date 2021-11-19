# import json, sys
# from datetime import datetime
# import matplotlib.pyplot as plt
# import pandas as pd
# from nltk.corpus import stopwords
# import re 
# from nltk.tokenize import word_tokenize
# from nltk import SnowballStemmer
# from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
# from sklearn.multiclass import OneVsRestClassifier
# from sklearn.linear_model import SGDClassifier
# from sklearn import metrics
# import numpy as np

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re, sys, os, json
import datetime as dt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.metrics import f1_score,precision_score,recall_score
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from datetime import datetime

DATA_DIRECTORY = "../Results"
RES_DIR = "../Results"
fpath = f"{DATA_DIRECTORY}/{sys.argv[1]}/Posts/posts.json"

with open(fpath, "r", encoding="utf8") as datajs:
    data_arr = json.load(datajs)["Posts"]

df = pd.DataFrame(columns=['title','tags'])
stemmer = SnowballStemmer('english')

stop_words = set(stopwords.words('english'))

def striphtml(data):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr,' ',str(data))
    return cleantext

for id, post in data_arr.items():
    title = post["title"]
    title=striphtml(title.encode('utf-8'))

    tags = post["tags"]
    tags = re.sub(r'[<>]',' ',tags)
    tags = ' '.join(tags.split())
    title = re.sub(r'[^a-zA-Z]+', ' ', title)
    
    words = word_tokenize(str(title.lower()))
    title = ' '.join(str(stemmer.stem(j)) for j in words if j not in stop_words and (len(j)!=1))
    df.loc[len(df)] = [title, tags]

df = df[['title', 'tags']]
df['title'] = df['title'].astype('str')
print(df)

y_vectorizer = CountVectorizer()
multilabel_output = y_vectorizer.fit_transform(df["tags"])

def tags_to_choose(n):
    """
    Choose first n tags only.
    """

    t = multilabel_output.sum(axis=0).tolist()[0]
    sorted_tags_i = sorted(range(len(t)), key=lambda i: t[i], reverse=True)
    multilabel_outputn=multilabel_output[:,sorted_tags_i[:n]]
    return multilabel_outputn


def questions_explained_fn(n):
    multilabel_outputn = tags_to_choose(n)
    x= multilabel_outputn.sum(axis=1)
    return (np.count_nonzero(x==0))

question_explained = []
total_tags = multilabel_output.shape[1]
total_qs = df.shape[0]

for i in range(500, total_tags, 100):
    question_explained.append(np.round(((total_qs-questions_explained_fn(i))/total_qs)*100,3))

multilabel_yx = tags_to_choose(5500)
print("number of questions that are not covered :", questions_explained_fn(5500),"out of ", total_qs)

multilabel_yx.get_shape()

print("Number of tags in sample :", multilabel_output.shape[1])

total_size=df.shape[0]
train_size=int(0.80*total_size)

x_train=df.head(train_size)
x_test=df.tail(total_size - train_size)

y_train = multilabel_yx[0:train_size,:]
y_test = multilabel_yx[train_size:total_size,:]

print("Number of data points in train data :", y_train.shape)
print("Number of data points in test data :", y_test.shape)

tfidf_vect = TfidfVectorizer(min_df=0.00009,max_features=200000,smooth_idf=True,norm='l2',\
               tokenizer=lambda x : x.split(),sublinear_tf=False, ngram_range=(1,3) )

x_train_vectors = tfidf_vect.fit_transform(x_train['title'])
x_test_vectors = tfidf_vect.transform(x_test['title'])

print("Dimensions of train data X:",x_train_vectors.shape, "Y :",y_train.shape)
print("Dimensions of test data X:",x_test_vectors.shape,"Y:",y_test.shape)

classifier = OneVsRestClassifier(SGDClassifier(loss='log', alpha=0.00001, penalty='l1'), n_jobs=-1)
x_train_vectors = np.array(x_train_vectors)
y_train = np.array(y_train)
print(len(x_train_vectors))
print(len(y_train))
classifier.fit(x_train_vectors,y_train)

predictions = classifier.predict(x_test_vectors)


print("accuracy ", metrics.accuracy_score(y_test,predictions))
print("macro f1 score ",metrics.f1_score(y_test,predictions, average='macro'))
print("micro f1 score ", metrics.f1_score(y_test, predictions, average='micro'))
print("hamming loss ", metrics.hamming_loss(y_test,predictions))
