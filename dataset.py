import json
from dateutil.parser import parse
from textblob import TextBlob
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk import ngrams
import string, os, math

class Preprocess:

	def __init__(self):
		self.stopwords = [str(word) for word in stopwords.words("english")]
		self.keyword_frequency = {}


	def sort_by_time(self, file):
		"""
		"""

		with open(file, 'r') as f:
			lines = f.readlines()

		tweets = {}

		for line in lines:
			tweet = json.loads(line)
			time = parse(tweet['created_at'])
			if time not in tweets:
				tweets[time] = []
				tweets[time].append(tweet)
			else:
				tweets[time].append(tweet)
			get_keywords(tweet)


		timestamps = []
		for time in tweets:
			timestamps.append(time)

		timestamps.sort()
		tweets_sorted_by_time = []

		for time in timestamps:
			tweets_sorted_by_time += tweets[time]

		with open("sorted1000.json", 'w') as f:
			f.writelines("%s\n" % str(_) for _ in tweets_sorted_by_time)


	def tokenize(self, file_content, file=None):
		"""
		Tokenize the content of the word
		:param file_content: the text content of a file
		:return: list of tokens obtained by using nltk.word_tokenize()
		"""
		# print(file)
		tokens = word_tokenize(file_content)
		tokens = [i for i in tokens if i not in string.punctuation]
		tokens = [word for word in tokens if len(word) > 1]
		return tokens


	def stem(self, tokens):
		"""
		Stemming of the tokens
		:param tokens: list of tokens to be stemmed down
		:return: list of stemmed tokens
		"""
		stemmed = []
		stemmer = PorterStemmer()
		for item in tokens:
			stemmed.append(stemmer.stem(item))
		return stemmed


	def generate_ngrams(self, tokens):
		"""
		Generate uni, bi and tri-grams from the stemmed down tokens of file text
		:param tokens: list of stemmed down tokens
		:return: list containing three separate lists - one each for unigram, bigram and trigram
		"""
		unigram = [' '.join(gram) for gram in ngrams(tokens,1)] 
		bigram = [' '.join(gram) for gram in ngrams(tokens, 2)]
		trigram = [' '.join(gram) for gram in ngrams(tokens, 3)]
		return [unigram, bigram, trigram]


	def keyword_for_tweets(self, file):
		"""
		"""
		with open(file, 'r') as f:
			lines = f.readlines()

		for line in lines:
			tweet = json.loads(line)
			id = tweet['id']
			txt = tweet['full_text']
			tokens = self.tokenize(txt, file)
			ngrams = self.generate_ngrams(tokens)
			ngrams[0] = self.stem(ngrams[0])
			keywords = ngrams[0]
			file_keywords = [word for word in keywords if word not in self.stopwords]
			for word in file_keywords:
				if word not in self.keyword_frequency:
					self.keyword_frequency[word] = {}
					self.keyword_frequency[word][id] = 1
				else:
					if id not in self.keyword_frequency[word]:
						self.keyword_frequency[word][id] = 1
					else:
						self.keyword_frequency[word][id] += 1

		for _ in self.keyword_frequency:
			print(_, self.keyword_frequency[_])



