"""Domaincheck.check unittestsw

"""
from unittest import TestCase
from domaincheck import check


class TestWhois(TestCase):
    """Test the ``whois`` function

    """

    def test_good_domain(self):
        """Test a good domain name

        """
        response = check.whois('google.com')
        self.assertTrue(response)

