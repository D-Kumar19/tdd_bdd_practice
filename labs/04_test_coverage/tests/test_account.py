"""
Test Cases TestAccountModel
"""
import json
from random import randrange
from unittest import TestCase
from models import db
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

class TestAccountModel(TestCase):
    """Test Account Model"""

    @classmethod
    def setUpClass(cls):
        """ Load data needed by tests """
        db.create_all()  # make our sqlalchemy tables
        global ACCOUNT_DATA
        with open('tests/fixtures/account_data.json') as json_data:
            ACCOUNT_DATA = json.load(json_data)

    @classmethod
    def tearDownClass(cls):
        """Disconnext from database"""
        db.session.close()

    def setUp(self):
        """Truncate the tables"""
        self.rand = randrange(0, len(ACCOUNT_DATA))
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """Remove the session"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_all_accounts(self):
        """Test creating multiple Accounts"""
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        self.assertEqual(len(Account.all()), len(ACCOUNT_DATA))

    def test_create_an_account(self):
        """Test account creation using known data"""
        data = ACCOUNT_DATA[self.rand]
        account = Account(**data)
        account.create()
        self.assertEqual(len(Account.all()), 1)

    def test_represent_as_string(self):
        """Test representing an account as a string"""
        account = Account(name = "Foo")
        self.assertEqual(str(account), "<Account 'Foo'>")

    def test_to_dict(self):
        """Test to dictionary"""
        data = ACCOUNT_DATA[self.rand]
        account = Account(**data)
        result = account.to_dict()
        self.assertEqual(result["name"], account.name)
        self.assertEqual(result["email"], account.email)
        self.assertEqual(result["phone_number"], account.phone_number)
        self.assertEqual(result["disabled"], account.disabled)

    def test_from_dict(self):
        """Test account creation from a dictionary"""
        data = ACCOUNT_DATA[self.rand]
        account = Account()
        account.from_dict(data)
        self.assertEqual(data["name"], account.name)
        self.assertEqual(data["email"], account.email)
        self.assertEqual(data["phone_number"], account.phone_number)
        self.assertEqual(data["disabled"], account.disabled)

    def test_update_an_account(self):
        """Test account update using know data"""
        data = ACCOUNT_DATA[self.rand]
        account = Account(**data)
        account.create()
        self.assertEqual(len(Account.all()), 1)

        account.disabled = True
        account.update()
        found = Account.find(account.id)
        self.assertTrue(found.disabled)

        account.name = "Bar"
        account.update()
        found = Account.find(account.id)
        self.assertEqual(found.name, "Bar")

        account.phone_number = "123-456-7890"
        account.update()
        found = Account.find(account.id)
        self.assertEqual(found.phone_number, "123-456-7890")

        account.email = "hello@gmail.com"
        account.update()
        found = Account.find(account.id)
        self.assertEqual(found.email, "hello@gmail.com")

        account.id = None
        account.name = "Foo"
        self.assertRaises(DataValidationError, lambda: account.update())

    def test_update_without_an_id(self):
        """Test update without an id"""
        account = Account()
        account.id = None
        self.assertRaises(DataValidationError, lambda: account.update())

    def test_delete_an_account(self):
        """Test account deletion"""
        data = ACCOUNT_DATA[self.rand]
        account = Account(**data)
        account.create()
        self.assertEqual(len(Account.all()), 1)

        account.delete()
        self.assertEqual(len(Account.all()), 0)
