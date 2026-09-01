from django.db import models                         # Imports Django's tools for creating database models

from django.contrib.auth.models import User         # Imports Django's built-in User model


# Create your models here.
class Category(models.Model):                        # Creates a Category model/table in the database

    name = models.CharField(max_length=100)          # Creates a text field called "name", with a maximum of 100 characters

    def __str__(self):                               # Defines what should be shown when a Category is displayed as text
        return self.name                              # Returns the category's name, e.g. "Food"


class Expense(models.Model):                         # Creates an Expense model/table in the database

    user = models.ForeignKey(                        # Creates a relationship between Expense and User
        User,                                        # Says this expense belongs to a User
        on_delete=models.CASCADE                    # Deletes the expense if its User is deleted
    )

    category = models.ForeignKey(                   # Creates a relationship between Expense and Category
        Category,                                    # Says this expense belongs to a Category
        on_delete=models.CASCADE                    # Deletes the expense if its Category is deleted
    )

    amount = models.DecimalField(                    # Creates a field for storing the expense amount
        max_digits=10,                               # Allows a maximum of 10 digits in total
        decimal_places=2                             # Allows 2 digits after the decimal point, e.g. 500.50
    )

    description = models.CharField(                 # Creates a text field for describing the expense
        max_length=255                               # Allows the description to contain up to 255 characters
    )

    date = models.DateField()                       # Creates a field for storing the date of the expense

    def __str__(self):                               # Defines how an Expense should be displayed as text
        return f"{self.description} - {self.amount}" # Displays something like "Lunch - 500.00"

