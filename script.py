import urllib2 # For requesting
from bs4 import BeautifulSoup
import json

import utilities as u

def main():


	lineNum = 1552

	with open('./recipes/duplicateData.txt') as fileID:
		for i, line in enumerate(fileID):
			if i == lineNum:
				ingredients =  json.loads(line)["ingredients"]
				for ingr in ingredients:
					print ingr
					print splitIngredientString(ingr)
				break


def splitIngredientString(ingr):
	"""Splits the ingredient into amount, unit and ingredient name."""
	splitList = []



	return splitList

if __name__ == '__main__':
	main()