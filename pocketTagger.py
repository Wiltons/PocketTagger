import json
import operator
import re
import tempfile
import urllib
import urllib2
from time import strftime

apikey = 'cH6gdvT0p0xK4Vc61aT7779o2cAqN8aM'
index_url = u'https://getpocket.com'
read_api_url = index_url + u'/v3/get'
modify_api_url = index_url + u'/v3/send'
only_pull_tag = None
articles = []
# Fill in username and password
username = ''
password = ''
# Wordcount parameters for tagging
shortSize = 2000
longSize = 10000
# Set to true/false to only tag long or short
tagLong = True
tagShort = True

def get_auth_uri():
	#Quick function to return the authentication part of the url
	uri = ""
	uri = u'{0}&apikey={1!s}'.format(uri, apikey)
	if not username or not password:
		print('Username or password is blank.')
	else:
		uri = u'{0}&username={1!s}'.format(uri, username)
		uri = u'{0}&password={1!s}'.format(uri, password)
	return uri
	
def get_pull_articles_uri():
	uri = ""
	uri = u'{0}&state={1}'.format(uri, u'unread')
	uri = u'{0}&contentType={1}'.format(uri, u'article')
	if only_pull_tag is not None:
		uri = u'{0}&tag={1}'.format(uri, only_pull_tag)
	return uri
	
def fetch_items_short():
	pocket_feed = []
	fetch_url = u"{0}?{1}{2}".format(
		read_api_url,
		get_auth_uri(),
		get_pull_articles_uri()
	)
	shortItems = []
	#print(fetch_url)
	try:
		request = urllib2.Request(fetch_url)
		response = urllib2.urlopen(request)
		pocket_feed = json.load(response)['list']
	except urllib2.HTTPError as e:
		#self.log.exception("Pocket returned an error: {0}".format(e.info()))
		print('Pocket returned an error: {0}'.format(e.info()))
		return []
	except urllib2.URLError as e:
		#self.log.exception("Unable to connect to getpocket.com's api: {0}\nurl: {1}".format(e, fetch_url))
		return []

	for pocket_article in pocket_feed.iteritems():
		#print ('Item id is {0} and is length {1}'.format(pocket_article[1]['item_id'],pocket_article[1]['word_count']))
		if (int(pocket_article[1]['word_count']) <= shortSize):
			shortItems.append({
				'item_id': pocket_article[0],
				'title': pocket_article[1]['resolved_title'],
				'date': pocket_article[1]['time_updated'],
				'url': u'{0}/a/read/{1}'.format(index_url, pocket_article[0]),
				'real_url': pocket_article[1]['resolved_url'],
				'description': pocket_article[1]['excerpt'],
				'sort': pocket_article[1]['sort_id'],
				'size': pocket_article[1]['word_count']
			})
			#print('Added item {0}'.format(pocket_article[1]['resolved_url']))
		else:
			pass
				
	shortItems = sorted(shortItems, key=operator.itemgetter('sort'))
	return shortItems
	
def fetch_items_long():
	pocket_feed = []
	fetch_url = u"{0}?{1}{2}".format(
		read_api_url,
		get_auth_uri(),
		get_pull_articles_uri()
	)
	longItems = []
	#print(fetch_url)
	try:
		request = urllib2.Request(fetch_url)
		response = urllib2.urlopen(request)
		pocket_feed = json.load(response)['list']
	except urllib2.HTTPError as e:
		#self.log.exception("Pocket returned an error: {0}".format(e.info()))
		print('Pocket returned an error: {0}'.format(e.info()))
		return []
	except urllib2.URLError as e:
		#self.log.exception("Unable to connect to getpocket.com's api: {0}\nurl: {1}".format(e, fetch_url))
		return []

	for pocket_article in pocket_feed.iteritems():
		#print ('Item id is {0} and is length {1}'.format(pocket_article[1]['item_id'],pocket_article[1]['word_count']))
		if (int(pocket_article[1]['word_count']) >= longSize):
			longItems.append({
				'item_id': pocket_article[0],
				'title': pocket_article[1]['resolved_title'],
				'date': pocket_article[1]['time_updated'],
				'url': u'{0}/a/read/{1}'.format(index_url, pocket_article[0]),
				'real_url': pocket_article[1]['resolved_url'],
				'description': pocket_article[1]['excerpt'],
				'sort': pocket_article[1]['sort_id'],
				'size': pocket_article[1]['word_count']
			})
			#print('Added item {0}'.format(pocket_article[1]['item_id']))
		else:
			pass
				
	longItems = sorted(longItems, key=operator.itemgetter('sort'))
	return longItems
	
	
def tagItems(mark_list, tags=None):
	actions_list = []
	split_array = []
	for article_id in mark_list:
		actions_list.append({
			'action': 'tags_add',
			'item_id': article_id,
			'tags': tags
		})
		#print("Added {0}".format(article_id))
	
	#print(len(actions_list))
	if len(actions_list) > 50:
		chunks = (len(actions_list) / 50) + 1
		#print(chunks)
		split_array = split_list(actions_list, chunks)
		
	for partition in split_array:
		#print(len(partition))
		tag_url = u'{0}?actions={1}{2}'.format(
			modify_api_url,
			json.dumps(partition, separators=(',', ':')),
			get_auth_uri()
		)
		#print("Tag url: {0}".format(tag_url))
		try:
			request = urllib2.Request(tag_url)
			response = urllib2.urlopen(request)
		except urllib2.HTTPError as e:
			print('Pocket returned an error while archiving articles: {0}'.format(e))
			return []
		except urllib2.URLError as e:
			print("Unable to connect to getpocket.com's modify api: {0}".format(e))
			return []
	return []

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]

if tagLong:
	longList = fetch_items_long()
	tagItems([x['item_id'] for x in longList], ['very_long'])
if tagShort:
	shortList = fetch_items_short()
	tagItems([x['item_id'] for x in shortList], ['short'])
