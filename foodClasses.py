import utilities as u


class Recipe(object): # Make this a new-style
    """Class for storing recipes."""
    def __init__(self):
        """Initializes the class."""
        self.recipeName = ''  # Name of recipe
        self.ingredients = [] # List of ingredients
        self.steps = []       # List of steps
        self.time = 0         # Time of recipie in minutes
        self.isBroken = False # Initialize the recipie to broken

    def addStep(self, step, index = -1): 
        """Adds a step to the list at the index specified."""
        self.steps.append(step) # Add the step to the end

    def addIngredient(self, ingredient, index = -1): 
        """Adds a ingredient to the list of ingredients
        at the index specified.
        """
        self.ingredients.append(ingredient) # Add the ingredient to the end
        pass

    def __str__(self):
        """Prints the recipie as string my man."""
        if self.isBroken:
            return "Broken recipe!" # If the recipe is broken, return this string
        else:
            try:
                returnString = ""             # Start with empty

                # Add the name to the string
                returnString += self.recipeName + '\n'
                # Add the time to the string
                returnString += str(self.time) + '\n'
                for ingr in self.ingredients:
                    returnString += str(ingr) + '\n' # Add ingredient list first
                returnString += '\n'                 # Some space
                for step in self.steps:
                    returnString += str(step) + '\n' # Add the steps
                return returnString
            except UnicodeDecodeError: # If we cannot decode, declare the recipe a failure
                try:
                    return "UnicodeDecodeError in " + self.name
                except:
                    return "UnicodeDecodeError"

class Ingredient:
    """Ingredient class."""
    def __init__(self, ingredient, amount):
        """Initializes the name of ingredient, the amount
        and the unit.
        """
        self.ingredient = ingredient # A string
        self.amount = amount         # A float/integer

    def __str__(self):
        """String representation of the ingredient."""
        return self.ingredient + ' ' + str(self.amount) 

class Amount:
    """Class of amount. Number with unit."""
    def __init__(self, amount, unit):
        self.amount = amount
        self.unit = unit

    def __str__(self):
        return str(self.amount) + str(self.unit)

    def toGrams(self):
        """Converts weight measurments to grams."""
        pass


class Unit:
    """Class to keep track of units."""
    def __init__(self, unit):
        """Initializes the instance."""
        self.unit = unit  # Unit as string

