import json, sys
from pathlib import Path
from bs4 import BeautifulSoup
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

DATA_DIRECTORY = "../Data/Extracted"
RES_DIR = f"../Results/{sys.argv[1]}"
WORDS = 100
N_TOP = 10
Path(RES_DIR).mkdir(parents=True, exist_ok=True)
IGNORE_WORDS = ["doe"]

def getTfIdfFreq(opfl, fld):
    fpath = f"{DATA_DIRECTORY}/{sys.argv[1]}/{opfl}.json"
    with open(fpath, "r", encoding="utf8") as datajs:
        data_arr = json.load(datajs)["data"]

    lemma = nltk.wordnet.WordNetLemmatizer()
    def tokenize(text):
        tokens = nltk.word_tokenize(text)
        tokens=[tok.lower() for tok in tokens if tok.isalpha()]
        lemms = []
        for item in tokens:
            item_ = lemma.lemmatize(item)
            if item_ in IGNORE_WORDS:
                continue
            lemms.append(item_)
        return lemms

    tok_arr = []
    tok_dct = {}
    for user in data_arr:
        about = BeautifulSoup(user.get(fld, ""), "lxml").text
        tok_arr.append(about)
    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    tfs = tfidf.fit_transform(tok_arr)
    terms_r = tfs.sum(axis= 0)
    terms_r = [(terms_r[0, i], i) for i in range(terms_r.shape[1])]
    terms_r.sort(reverse= True)
    feat = tfidf.get_feature_names_out()

    top_terms = terms_r[:N_TOP]
    top_terms = {feat[term[1]]: term[0] for term in top_terms}
    fig = plt.figure(figsize=(12,6))
    plt.bar(top_terms.keys(), top_terms.values(), label="TF-IDF Score")
    plt.legend()
    plt.tight_layout(pad=0)
    plt.savefig(f"{RES_DIR}/MapReduce_Bar_{opfl}_{fld}.png")
    plt.clf()

    for term in terms_r:
        if len(feat[term[1]]) < 3:
            continue
        tok_dct[feat[term[1]]] = term[0]
    with open(f'{RES_DIR}/MapReduce_{fld}_{opfl}.json', "w") as mrjs:
        json.dump(tok_dct, mrjs, indent="\t")
    return tok_dct

def make_wordcloud(freq_dict, fln, fld):
    wc = WordCloud(width= 640, height= 640, prefer_horizontal= 1, max_words=WORDS).generate_from_frequencies(freq_dict)
    plt.figure(frameon=False)
    plt.axis("off")
    plt.imshow(wc, interpolation="bilinear")
    plt.savefig(f'{RES_DIR}/WordCloud_{fln}_{fld}.png', bbox_inches='tight')
    plt.clf()

if __name__ == "__main__":
    make_wordcloud(getTfIdfFreq("Users", "AboutMe"), "Users", "AboutMe")
    make_wordcloud(getTfIdfFreq("Posts", "Title"), "Posts", "Title")
    make_wordcloud(getTfIdfFreq("Posts", "Body"), "Posts", "Body")