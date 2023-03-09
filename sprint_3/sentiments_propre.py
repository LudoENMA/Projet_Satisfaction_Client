import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %matplotlib inline # ligne pour jupyter seulement 

import json
import networkx as nx
from nltk.tokenize import TweetTokenizer


df = pd.read_csv('PART2_Infos_generales_Commentaire.csv', sep = ',')


commentaires = df['Titre comment']


from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer

sentiment_intensity_analyzer = SentimentIntensityAnalyzer()

score = commentaires.apply(lambda x: sentiment_intensity_analyzer.polarity_scores(x))
scores = commentaires.apply(lambda x: sentiment_intensity_analyzer.polarity_scores(x)['compound'])


print(scores)
scores.describe()



tokenizer = TweetTokenizer()
texte = ' '.join(commentaires)
mots = tokenizer.tokenize(texte)
print(len(mots))

from collections import Counter

word_count = Counter([m.lower() for m in mots])

mots_tries = sorted(word_count, key=lambda x: word_count.get(x), reverse=True)

