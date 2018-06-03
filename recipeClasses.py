# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import foodClasses as fc
import utilities as u

class MatPratRecipe(fc.Recipe):
    """Recipe from www.matprat.no"""
    def __init__(self, url):
        """Initializes from url."""
        # Should have check that it is a valid URL from matprat.no
        super(MatPratRecipe, self).__init__()     # Initialize 
        soup = BeautifulSoup(data, 'html.parser') # Make soup
        ### ____ FIND INGREDIENTS ___ ###
        manyIngredients = soup.find_all("li", attrs = {"itemprop" : "ingredients"})
        for hit in manyIngredients:
            ingredientName = hit.contents[-1].replace('\r\n', '').encode('utf-8') # Extract the ingredient name 
            quantity = hit.find("span", class_ = "amount")["data-amount"].encode('utf-8')# Extract the quantity
            unit = hit.find("span", class_ = "unit")["data-unit"].encode('utf-8') # Extract the unit

            amount = fc.Amount(quantity, unit) # Make a new Amount instance
            newIngredient = fc.Ingredient(ingredientName, amount) # Make a new Ingredient instance
            self.addIngredient(newIngredient)  # Add the new ingredient to the recipe
        ### ____ FIND STEPS ____ ###
        manySteps = soup.find("div", class_ = "rich-text") # Find the div containint the steps
        manySteps = manySteps.find_all("p")                # Ordinary paragraph contains the steps
        for hit in manySteps:
            newStep = hit.string.encode('utf-8')            # Initial string of step
            newStep = self.fixStep(newStep)                # Fix the step
            if 'Slik gjør du:' in newStep:
                pass
            else:
                self.addStep(newStep)                          # Add the step to the list


        ### ____ FIND TIME ____ ###
        self.time = self.getTime(soup)

    def getTime(self, soup):
        """Finds the time interval from the soup."""
        time = soup.find("span", attrs = {"data-epi-property-name" : "RecipeTime"}) 
        time = time.string # Get the string
        time = time.split()[:-1][0].encode('utf8')
        time = time.split('\xe2\x80\x93')
        return time

    def fixStep(self, step):
        """Fixes the step string scraped from matprat.no.
        We basically want to remove the starting number from the strings
        1. Cut down carrots and pot them down.
        """
        if '. ' in step[0:5]:   # If this little string is somewhere in the start
            # We need to remove the starting number and stuff            
            step = step[2:]     # This works if there is under 9 steps
            if step[0] == ' ':  # If there were steps with number >= 10 there will be a space
                step = step[1:] # Cut the first space

        return step             # Return the fixed step

class AllRecipesRecipe(fc.Recipe):
    """Recipe from allrecipes.com."""
    def __init__(self, url, knownRecipes = []):
        """Initializes."""
        super(AllRecipesRecipe, self).__init__() # Initialize 
        self.url = url
        data = u.getData(url)   # Fetch the data
        if data is None:
            self.isBroken = True # Set the recipie to broken
            return               # End the rest of the stuff
        else:
            soup = BeautifulSoup(data, 'html.parser') # Make soup

            self.findName(soup)
            if self.recipeName in knownRecipes:       # If the recipe is already found, abort immidietly
                self.isBroken = True
                return None
            self.findTime(soup)                    # Find the time
            self.findIngredients(soup)
            self.findSteps(soup)

    def findName(self, soup):
        """Finds the name of the recipe."""
        ### ____ FIND RECIPE NAME ____ ###
        name = soup.find("h1", class_ = "recipe-summary__h1").string # Find the recipe name
        name = u.unicodeToASCII(name)
        self.recipeName = name.encode('utf-8') # Add the recipe name

    def findTime(self, soup):
        """Finds the time for recipe from the soup."""
        ### ____ FIND TIME ____ ###
        time = soup.find("span", class_ = "ready-in-time") # This is where the time should be
        if time is None:                                   # If time is somewhere else, we will find none
            return                                         # Give up if we do not find it
        try:                                               # Here we catch any other general error
            self.time = u.unicodeToASCII(time.string)      # If everything is good, add the time to the instance
        except AttributeError:                             # if we encounter an error
            pass                                           # Ignore it

    def findIngredients(self, soup):
        """Finds the ingredients from the soup."""
        ### ____ FIND INGREDIENTS ____ ###
        ingredients = soup.find_all("span", class_ = "recipe-ingred_txt added")
        for ingr in ingredients:
            ingr = u.unicodeToASCII(ingr.string)
            self.addIngredient(ingr)

    def findSteps(self, soup):
        """Finds the steps of the recipe."""
        ### ____ FIND STEPS ____ ###
        steps = soup.find_all("span", class_ = "recipe-directions__list--item")
        for step in steps:
            newStep = step.string
            if newStep is not None:
                newStep = u.unicodeToASCII(newStep).replace('\n', '')
                self.addStep(newStep)

    def asDict(self):
        """Makes the recipe into a dictionary for json formating.
        Other than parent class because of 'url'.
        """
        dicty = super(AllRecipesRecipe, self).asDict()
        dicty["url"] = self.url
        return dicty
