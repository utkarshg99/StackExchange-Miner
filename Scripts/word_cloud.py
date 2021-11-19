import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import wordcloud


STACKEXCHANGES = ["history.stackexchange.com"]
for x in STACKEXCHANGES:
    word_counts = {}
    fpath = "../Results/" + x + "/Tags/counts.csv"
    df = pd.read_csv(fpath)
    # print(df)
    for i in df.index:
        cur_row = df.loc[i]
        item = cur_row['id']
        # if item == "africa": break
        # print(item)
        # print(cur_row.keys())
        if item not in word_counts.keys():
            word_counts[item] = int(cur_row['value'])
        else:
            word_counts[item] += int(cur_row['value'])
    print(len(word_counts))
    print(word_counts)
    word_cloud = WordCloud(width=900,height=500, max_words=100,relative_scaling=1,normalize_plurals=False).generate_from_frequencies(word_counts)


    # Display the generated image:
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
