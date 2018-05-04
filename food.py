from bs4 import BeautifulSoup
import re

import utilities as u
import foodClasses as fc   # Classes to use 
import recipeClasses as rc # Classes of Recipes


def main():
    url  = 'https://www.allrecipes.com/recipe/8720/honey-mustard-grilled-chicken/'


    k = 0
    n = 1
    fileID = open('recipeData.txt', 'w')
    while True:
        soup = "https://www.allrecipes.com/recipes/17562/?page=" + str(n) # list of many recipes
        soup = u.getData(soup)
        soup = BeautifulSoup(soup, 'html.parser')
        links = soup.find_all("h3", class_ = "fixed-recipe-card__h3")
        for link in links:
            k += 1
            url = link.find("a")["href"]
            rec = rc.AllRecipeRecipe(url)
            fileID.write(str(rec) + '\n')
            try:
                print k
            except IOError:
                pass
        n += 1

if __name__ == '__main__':
    main()
