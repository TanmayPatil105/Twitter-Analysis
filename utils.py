from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import nltk
import regex as re
import pandas as pd
import string
nltk.download('words')
nltk.download('stopwords')

#
# remove punctuation
#
def remove_punctuation(word_list):
    list = list(string.punctuation)
    return [w for w in word_list if w not in list]

#
# preprocess data
#
def preprocess():
    tweets = pd.read_csv('Dataset.csv')

    # extract hashtags
    tweets['hashtag'] = tweets['Tweet'].apply(lambda x: re.findall(r"#(\w+)", x))

    # change to lowercase
    tweets['Tweet'] = tweets.Tweet.str.lower()

    # remove non alpha-numeric words
    tweets.Tweet = tweets.Tweet.apply(lambda x:re.sub('[^a-zA-Z0-9]',' ',x))

    # remove non-english words
    words = set(nltk.corpus.words.words())
    tweets.Tweet = tweets.Tweet.apply(lambda x:" ".join(w for w in nltk.wordpunct_tokenize(x) if w.lower() in words or not w.isalpha()))

    # removing hyperlinks
    tweets.Tweet = tweets.Tweet.apply(lambda x: re.sub(r'https?:\/\/\S+', '', x))
    tweets.Tweet.apply(lambda x: re.sub(r"www\.[a-z]?\.?(com)+|[a-z]+\.(com)", '', x))
    tweets.to_csv('Dataset.csv', index=False)

    # remove video links
    tweets.Tweet = tweets.Tweet.apply(lambda x: re.sub(r'{link}', '', x))
    tweets.Tweet = tweets.Tweet.apply(lambda x: re.sub(r"\[video\]", '', x))

    # remove non-letter characters
    tweets.Tweet = tweets.Tweet.apply(lambda x: re.sub(r'\W', ' ', x))

    # remove punctuation
    tweets['Tweet'] = tweets['Tweet'].str.replace('[^\w\s]','')

    # remove stop words
    stop = stopwords.words('english')
    tweets['Tweet'] = tweets['Tweet'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

    # remove mentions @
    tweets.Tweet = tweets.Tweet.apply(lambda x: re.sub(r'@mention', '', x))

    # remove timestamps in the Date 
    tweets['Date Created'] = tweets['Date Created'].str.split(' ').str[0]

    # tokenize tweets
    tknzr = TweetTokenizer()
    tweets['Tweet_tokens'] = tweets['Tweet'].apply(tknzr.tokenize)

    tweets.to_csv('Preprocessed.csv')
