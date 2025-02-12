from django.test import TestCase
from .models import UserAccount
from django.urls import reverse

"""
IMPORTANT NOTES:
= A temporary database (with the same model structure but no data) is created for each test.
= The regular Django database is unaffected.
= Use "python manage.py test core_app" to run the tests listed here.
"""

# Create your tests here.


def create_user(username:str, email:str, password:str):
    """
    This is a helper function that adds a user account to the (temporary testing) database using the given parameters.
    It can be called by the test functions to create a test user for them.
    It returns True if the test user was created successfully, and False if it wasn't.

    Within the same test function, try not to create accounts with the same username or email.
    """
    try:
        # Tries to create a new account with the parameters.
        testUser = UserAccount(username=username, email=email)
        testUser.set_password(password)
        testUser.save() # Saves the account to the testing database.
        return True
    except:
        # If any error or excpetion is thrown.
        print("An error or exception occurred while creating a user account.")
        return False
    

class LoginViewTests(TestCase):
    """
    Every test function in Django needs to be part of a class that inherits from the django.test.TestCase superclass.
    """

    def test_login_without_account(self):
        """
        Tests that users cannot log in with a username or email that doesn't belong to any existing accounts.
        They should be returned to the login page, and the response should have a status code of 200.
        """
        url = reverse("core_app:login", args=())
        # reverse() is useful if you want to call view functions that take arguments other than the request itself.
        data = {"username" : "Non-Existent-Username", "email" : "non@existent.Email", "password" : "password"}
        # Creates the request.POST dictionary that would come as part of a POST request (a.k.a the POST request variables).

        response = self.client.post(url, data)
        # Use "self.client.get()" if you are testing a GET request rather than a POST request.
        # If you don't want to use the reverse() function, then use "response = self.client.post("login/", data)" instead:

        self.assertEqual(response.status_code, 200)
        # Similar to JUnit's version, assertEqual() asserts that it's first argument is equal to the second.
