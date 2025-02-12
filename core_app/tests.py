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
    This is the class for the login_view() tests
    """

    def test_login_without_account(self):
        """
        Tests that users cannot log in with a username or email that doesn't belong to any existing accounts.
        They should be returned to the login page, and the response should have a status code of 200.
        """
        url = reverse("login", args=())
        # reverse() is useful if you want to call view functions that take arguments other than the request itself.
        data = {"username" : "Non-Existent-Username", "email" : "non@existent.Email", "password" : "password"}
        # Creates the request.POST dictionary that would come as part of a POST request (a.k.a the POST request variables).

        response = self.client.post(url, data)
        # Use "self.client.get()" if you are testing a GET request rather than a POST request.
        # If you don't want to use the reverse() function, then use "response = self.client.post("login/", data)" instead:

        self.assertEqual(response.status_code, 200)
        # Similar to JUnit's version, assertEqual() asserts that it's first argument is equal to the second.
        
        # Since no accounts have been created during this test, there are no accounts to log into.
        # Therefore, the login should fail, the user should be returned to the login page, and the status code should be 200.

    def test_login_with_wrong_password(self):
        """
        Tests that users cannot login using the wrong password for an existing account.
        They should be returned to the login page, and the response should have a status code of 200.
        """
        create_user("user001", "001@email.com", "password001")
        # Creates a user with the given username, email and password.

        url = reverse("login")
        data = {"username" : "user001", "email" : "001@email.com", "password" : "password002"}
        # Simulate logging in with the following details.
        # Note: as of 12/02/25, login_view() only uses the user's username (not their email) when logging in.

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        # The username and email given belong to an existing account, but the password given is incorrect.
        # Therefore, the login should fail, the user should be returned to the login page, and the status code should be 200.

    def test_login_with_correct_password(self):
        """
        Tests that users can log in successfully, using the username/email and password of an existing account.
        They should be redirected to the home page, and the response should have a status code of 302.
        """
        create_user("user001", "001@email.com", "password001")
        
        url = reverse("login")
        data = {"username" : "user001", "email" : "001@email.com", "password" : "password001"}

        response1 = self.client.post(url, data)

        self.assertEqual(response1.status_code, 302)
        # The username and email given belong to an existing account, and the password given is correct.
        # Therefore, the login should succeed, the user should be redirected to the home page, and the status code should be 302.

        response2 = self.client.post(url, data, follow=True)
        # For redirects in particular, if you wanted to get a regular response (containing the HTML content of the page),
        # then add "follow=True" to "self.client.post()".
        # For regular responses (where you use render() to return a HTML template), you don't need to do this.        

        self.assertContains(response2, "This is the super temporary home page")
        # assertContains() asserts that the first argument contains the second.
        # The user should be redirected to the home page, which contains the text "This is the super temporary home page".
        