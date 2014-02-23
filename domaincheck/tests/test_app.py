"""Domaincheck.app unittests

"""
from flask import url_for
from unittest2 import TestCase
from domaincheck import app

class TestMain(TestCase):
    """Test the ``/main`` route

    """

    def setUp(self):
        """Test setup, generate a test client

        """
        self.test_client = app.test_client()

    def test_main(self):
        """Test the route

        """
        with app.test_request_context():
            response = self.test_client.get(url_for('main'))

        self.assertEqual(response.status_code, 200, response.data)

class TestCheck(TestCase):
    """Test the main ``/check`` route

    """

    def setUp(self):
        """Test setup, generate a test client

        """
        self.test_client = app.test_client()

    def test_check_good_domain(self):
        """Test checking a good domain

        """

        with app.test_request_context():
            response = self.test_client.get('/check/example.com')
        self.assertEqual(response.status_code, 200, response.data)

