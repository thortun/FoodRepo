from bs4 import BeautifulSoup

import utilities as u

soup = u.getData('http://www.paulgraham.com/articles.html')
soup = BeautifulSoup(soup, 'html.parser')

links = soup.find_all("td", attrs = {"width" : "435"})

with open('input.txt', 'w') as fileID:
	for l in links:
		try:
			l = l.find("a")
			root = "http://www.paulgraham.com/"
			branch = l["href"]
			if 'http' in branch:
				pass
			else:
				fullLink = root + branch
				pageSoup = u.getData(fullLink)
				pageSoup = BeautifulSoup(pageSoup, 'html.parser')
				text = pageSoup.find("font").get_text()
				fileID.write(text + '\n')

		except:
			pass