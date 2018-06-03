from bs4 import BeautifulSoup
import re
import json
from urllib2 import HTTPError
import socket
import sys

import utilities as u
import foodClasses as fc   # Classes to use 
import recipeClasses as rc # Classes of Recipes


def main():
    recipeDataFile = open('recipes/recipeData.txt', 'a')              # This is where we write the actual recipes in json format
    with open('recipes/recipeNumber.txt', 'r') as recipeNumberFile:   # Open the file containing the recipe number
        recipeNumber = int(recipeNumberFile.read())                   # Set the recipe number
        recipeNumberFile.close()                                      # Close the file

    with open('recipes/foundRecipes.txt', 'r') as foundRecipesFile:        # This is a file with which recipe name we have encountered on each line
        writtenRecipes = set([recipeName.replace('\n', '') for recipeName in foundRecipesFile])   # A set to keep track of which recipes we have found to test for membership
        foundRecipesFile.close()

    foundRecipesFile = open('recipes/foundRecipes.txt', 'a')

    while True:
        printNumber(recipeNumber) # Print the current recipe number
        url = "https://www.allrecipes.com/recipe/" + str(recipeNumber)
        try:
            rec = rc.AllRecipesRecipe(url)                     # Fetch recipe
            if rec.isBroken:                                   # If the recipe is broke, just keep going
                print 'is a duplicate!', 
                recipeNumber += 1
                continue
            if rec.recipeName not in writtenRecipes:           # Test whether we have found this recipe before
                writtenRecipes.add(rec.recipeName)          # Add this recipe to the ones we have found
                recipeDataFile.write(json.dumps(rec.asDict()) + '\n')  # Write the recipe to the file in json format
                foundRecipesFile.write(rec.recipeName + '\n')  # Add thie recipe name to the list of found recipes
            else:
                print ' is a duplicate!',

        except (ValueError, TypeError):                                     # If we get an error in the making of recipe we skip it
            print ' made an error!'
            recipeNumber += 1                                  # Skip this recipe and continue the loop
            continue                                           # Continue the loop

        except:                                             # If we are locked out of the site or interrupt the fetching
            print "Unexpected error:", sys.exc_info()[0]
            with open('recipes/recipeNumber.txt', 'w') as recipeNumberFile:   # Open the file containing the recipe number
                recipeNumberFile.write(str(recipeNumber))                     # Set the recipe number
                recipeNumberFile.close()                                      # Save what we have to file and continue later
                exit(0)                                                       # Exit the program

        print ' '
        recipeNumber += 1

def printNumber(number):
    """Prettifying method."""
    try:
        print number,
    except IOError:
        pass

if __name__ == '__main__':
    main()
