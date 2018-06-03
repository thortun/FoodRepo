import urllib2      # Most URL-handeling happens here
import unicodedata  # To make unicode to only ascii

from math import ceil

def getElementsByProperty(HTMLData, HTMLTag, prop, propName):
    """Gets all HTMLTags with the given property and name.
    <HTMLTab prop="propName">*INNER HTML*</HTMLTag>
    Like this my friend.
    """
    allInstances = extractBetween(HTMLData, '<' + HTMLTag, '</' + HTMLTag + '>')
    if prop == '' and propName == '': # If both of these are emptry, we search only for the tag!
        thing = ''
    else:
        thing = prop + '="' + propName + '"' # Thing to check if is in HTMLstring
    if isinstance(allInstances, list): # If we have only one HTMLTag, it is not a list
        # Cut all hits without the id
        allInstances = [entry for entry in allInstances if thing in entry]
        for i, entry in enumerate(allInstances): # Go through every thing
            allInstances[i] = '<' + HTMLTag + entry + '</' + HTMLTag + '>' # Add back the HTML-tags
        return allInstances # Return the correct list

    elif isinstance(allInstances, str): # If there is just one HTMLTag found
        allInstances = '<' + HTMLTag + allInstances + '</' + HTMLTag + '>' # Add back the tags
        if thing not in allInstances: # If it does NOT contain the id
            return []           # Return an empty list 
        else:                   # If it contains the id
            return allInstances # Return the thing we found

def extractBetween(line, left, right, return_index = False):
	"""Extract all information between 'left' and 'right' in the string 'line'

	If optional parameter 'return_index' is True then we also return the index 
	where we found the extraction. This helps with placing the Actions
	header in the creature PDF.
	"""
	elements = [] # List containing all strings laying between 'left' and 'right'
	found = False # In the start we have yet to find a match for 'first'
	s = "" # Temporarry string to hold the stuff between left and right
	index_list = [] # A list of the index of where we found a match

	len_left = len(left)
	len_right = len(right)
	len_line = len(line)
	for i in xrange(0, len_line):
		# Search for the start left
		if line[i:(i + len_left)] == left:
			index_list.append(i) # Append the index where we found a match
			found = True

		# We only care wether we found a match for 'right' if we already have
		# a match for 'left'
		if line[i:(i + len_right)] == right and found:
			found = False # Next search
			elements.append(s) # Append
			s = "" # Clear temp string

		# We have found a match for our search, start adding it to a temporary string
		if found:
			s += line[i]

	# We have added a bit too much to the return-strings, namely
	# we started adding characters to the matches the second we found
	# the START of 'left' in the string, so we cut that away
	for i in xrange(0, len(elements)):
		elements[i] = elements[i][len(left):]

	# If there is only one element in the list, return this element, and 
	# if we are supposed to return the index list, we do that
	if len(elements) == 1:
		if return_index:
			return elements[0], index_list
		else:
			return elements[0]
	else:
		if return_index:
			return elements, index_list
		else:
			return elements

def getData(url):
    """Gets the HTML-data from the web-page url.
    returns None if there is a urllib.HTTPError
    """
    hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)

    try:
        page = urllib2.urlopen(req)      # Send a request
    except urllib2.HTTPError, e:
        print("Error fetching " + url)
        return None

    # Place all the data in a single string
    HTML_data = ""
    for line in page:
    	HTML_data += cropWhites(line) # Remove excess white spaces
    return HTML_data

def getElementsById(HTMLData, HTMLTab, identity):
    """Gets all the data for an element with id 'identity'"""
    return getElementsByProperty(HTMLData, HTMLTag, 'id', identity)

def getElementsByClass(HTMLData, HTMLTag, className):
    """Gets a HTML-element with class 'classname'."""
    return getElementsByProperty(HTMLData, HTMLTag, 'class', className)

def cropWhites(line):
    """Crops all whites spaces at the start and end of a line."""
    if len(line) == 0: # If there is no line, return empty string
        return ''
    while line[0] == ' ': # While there is a white space at the start
        line = line[1:]   # Crop white space from start
    while line[len(line) - 1] == ' ':
        line = line[-1:]  # Crop the last element if it is a white space
    return line

def unicodeToASCII(line):
    """Fixes some problems when writing and stuff."""
    return unicodedata.normalize('NFKD', line).encode('ascii', 'ignore')