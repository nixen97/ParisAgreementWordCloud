#!/usr/bin/env python3

import csv
import PyPDF2
import textract
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter


def main():

    text = ""

    with open("paris.pdf", "rb") as file:
        reader = PyPDF2.PdfFileReader(file)
        for p in range(reader.getNumPages()):
            page = reader.getPage(p)
            text += page.extractText()

    tokens = map(lambda x: x.lower(), word_tokenize(text))

    sw = stopwords.words('english')
    #sw.extend([',', '.', ';', ':', '(', ')'])
    sw.extend(map(str, list(range(10, 100))))
    sw.extend(map(chr, list(range(33, 127))))
    sw.remove('should')

    kws = [word for word in tokens if word not in sw]

    freqs = Counter(kws)
    
    wc = WordCloud(
        height=1080, width=1920,
        max_font_size=150, max_words=100, background_color='white'
    ).generate_from_frequencies(freqs)
    

    #Save wordcloud to file
    wc.to_file('wordcloud.png')

    #Save raw output to file
    with open('wordcloud_vals.csv', 'w') as file:
        w = csv.writer(file)
        for key, val in freqs.items():
            w.writerow([key, val])

    plt.imshow(wc)
    plt.axis('off')
    #plt.show()


if __name__ == '__main__':
    main()