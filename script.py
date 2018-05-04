import urllib2 # For requesting

def main():
	api_key = '9ca9e5104d5bd6289bbb72f8cd24574e'  # Api_key
	hdr = {} 

	url = 'http://food2fork.com/api/get'       # Base for requests

	rId = str(37859)

	# reqUrl = url + '?key=' + api_key + '&rId=' + rId
	reqUrl = 'http://food2fork.com/api/search?key=%s&q=shredded' % api_key
	print reqUrl


	req = urllib2.Request(reqUrl, headers = hdr)

	print urllib2.urlopen(req)

if __name__ == '__main__':
	main()