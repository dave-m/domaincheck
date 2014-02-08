"""Domaincheck.check unittestsw

"""
from unittest2 import TestCase
from domaincheck import check

GOOD_DOMAIN = 'google.com'
BAD_DOMAIN = 'ihopethisdoesnt.existever'


class TestWhois(TestCase):
    """Test the ``whois`` function

    """

    def test_good_domain(self):
        """Test a good domain name

        Ensure we get back a string with some contents

        """
        response = check.whois(GOOD_DOMAIN)
        self.assertTrue(response)
        self.assertIsInstance(response, basestring)

    def test_bad_domain(self):
        """Test a bad domain

        Ensure we get back an empty string

        """
        response = check.whois(BAD_DOMAIN)
        self.assertFalse(response)
        self.assertIsInstance(response, basestring)


class TestGetA(TestCase):
    """Test the ``get_a`` function

    """

    def test_good_domain(self):
        """Test with a known good domain

        We should get back a list of records (strings)

        """
        response = check.get_a(GOOD_DOMAIN)
        self.assertIsInstance(response, list)

        for record in response:
            # TODO: Could check for ipv4/ipv6 but currently
            # we only care if we get something
            self.assertIsInstance(record, basestring)

    def test_bad_domain(self):
        """Test a known bad domain

        We should get back an empty list

        """
        response = check.get_a(BAD_DOMAIN)
        self.assertIsInstance(response, list)
        self.assertFalse(response)

class TestGetMX(TestCase):
    """Test the ``get_mx`` function

    """

    def test_good_domain(self):
        """Test with a known good domain

        We should get back a sorted list of tuples,
        each of which contain the Exchange (string) and
        preference (int)

        """
        response = check.get_mx(GOOD_DOMAIN)
        self.assertIsInstance(response, list)

        for record in response:
            self.assertIsInstance(record, tuple)
            self.assertIsInstance(record[0], basestring)
            self.assertIsInstance(record[1], int)

    def test_bad_domain(self):
        """Test a known bad domain

        We should get back an empty list

        """
        response = check.get_mx(BAD_DOMAIN)
        self.assertIsInstance(response, list)
        self.assertFalse(response)

class TestGetNS(TestCase):
    """Test the ``get_ns`` function

    """

    def test_good_domain(self):
        """Test with a known good domain

        We should get back a list of records (strings)

        """
        response = check.get_ns(GOOD_DOMAIN)
        self.assertIsInstance(response, list)

        for record in response:
            # TODO: Could check for ipv4/ipv6 but currently
            # we only care if we get something
            self.assertIsInstance(record, basestring)

    def test_bad_domain(self):
        """Test a known bad domain

        We should get back an empty list

        """
        response = check.get_ns(BAD_DOMAIN)
        self.assertIsInstance(response, list)
        self.assertFalse(response)

class TestFullSearch(TestCase):
    """Test the ``full_search`` function

    """

    def test_good_domain(self):
        """Test with a known good domain

        We should get back a dictionary with the following keys:
            'a', 'mx', 'whois', 'nameservers'

        """
        response = check.full_search(GOOD_DOMAIN)
        self.assertIsInstance(response, dict)

        self.assertEqual(sorted(response.keys()),
                sorted(['a', 'mx', 'whois', 'nameservers']))

    def test_bad_domain(self):
        """Test a known bad domain

        We should get back a dictionary with the following keys:
            'a', 'mx', 'whois', 'nameservers'

        but with empty contents

        """
        response = check.full_search(BAD_DOMAIN)
        self.assertIsInstance(response, dict)

        self.assertEqual(sorted(response.keys()),
                sorted(['a', 'mx', 'whois', 'nameservers']))

        self.assertFalse(response['a'])
        self.assertFalse(response['mx'])
        self.assertFalse(response['nameservers'])
        self.assertIsInstance(response['whois'], basestring)
        self.assertFalse(response['whois'])

