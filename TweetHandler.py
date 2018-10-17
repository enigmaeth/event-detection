import json, datetime
from bisect import bisect_right
from dataset import Preprocess
from dateutil.parser import parse


class TweetHandler:
	def __init__(self, file):
		self.file = file
		self.times = self.initialize_times()
	
		
	def get_sorted_tweets(self):
		"""
		sorted by time in increasing order
		"""
		with open(self.file, 'r') as f:
			return f.readlines()
	
		
	def initialize_times(self):
		with open(self.file, 'r') as f:
			return [parse(json.loads(line)['created_at']) for line in f.readlines()]
	
	
	def get_index(self, time_):
		"""
		upper_bound: Find rightmost value less than or equal x
		"""
		time_ = datetime.datetime.strptime(time_, '%a %b %d %H:%M:%S %z %Y')
		i = bisect_right(self.times, time_)
		if i:
			return i-1
		raise ValueError

	
	def get_keywords(self, time_1, time_2):
		tweets = self.get_sorted_tweets()
		time_start = self.get_index(time_1)
		time_end = self.get_index(time_2)
		return Preprocess().keyword_for_tweets(tweets, time_start, time_end)
