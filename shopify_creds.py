#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Shopify Credential Object"""

import logging
import os
from ConfigParser import SafeConfigParser  # todo make Py 3.5x happy


class ShopifyCreds(object):

    """Credential Object to simply holds the creds"""

    SHOPIFY_KEY = None
    SHOPIFY_PASSWORD = None
    SHOPIFY_STORE = None
    SHOPIFY_BASE_URL = None
    overwrite_files = False  # flag used by write_json() and ETL application.

    expected_properties = [
        'SHOPIFY_KEY',
        'SHOPIFY_PASSWORD',
        'SHOPIFY_STORE',
        'SHOPIFY_BASE_URL',
    ]

    def __init__(self, creds=None):
        """
        Carburetor for the credential object
        :param creds: optional, dictionary of credential information
        :return: void
        """
        if isinstance(creds, dict):
            self.assign_creds(creds)
        else:
            self.assign_creds(self.get_creds_from_config())

    def assign_creds(self, creds):
        """
        Assign credentials from a dict
        :param creds:
        :return:
        """
        self.SHOPIFY_KEY = creds.get('SHOPIFY_KEY', None)
        self.SHOPIFY_PASSWORD = creds.get('SHOPIFY_PASSWORD', None)
        self.SHOPIFY_STORE = creds.get('SHOPIFY_STORE', None)
        self.SHOPIFY_BASE_URL = creds.get('SHOPIFY_BASE_URL', None)

        # iD10t check
        for item in self.expected_properties:
            error_count = 0
            if not hasattr(self, item):
                logging.error('Missing %s property in ShopifyCreds object', item)
                error_count += 1
        if error_count > 0:
            return False
        return True

    @classmethod
    def get_creds_from_config(cls):

        """
        Get a cred dict from custom function or cfg or freak out
        :return: dict
        """
        file_loc = os.path.dirname(os.path.realpath(__file__)) + '/config.cfg'
        parser = SafeConfigParser()
        parser.optionxform = str  # preserve case
        parser.read(file_loc)
        creds = dict(parser.items('all'))
        return creds
