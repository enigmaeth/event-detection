from TweetHandler import TweetHandler


if __name__ == '__main__':

	# file has sorted tweets
	file = './temp.json'
	time_1 = 'Thu Oct 11 07:30:50 +0000 2012'
	time_2 = 'Thu Oct 11 10:30:50 +0000 2012'
	th = TweetHandler(file)
	keywords = th.get_keywords(time_1, time_2)
	for key, val in keywords.items():
		print(key,': ', val)
