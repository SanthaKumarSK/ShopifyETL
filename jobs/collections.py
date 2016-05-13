#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Collection data extraction"""

from __future__ import print_function
from time import sleep
import logging
from shopify import Shopify
from util import write_json


class ExtractCollectionData(Shopify):

    """Extract Collection Data"""

    # int for seconds between page calls
    sleep_interval = 1
    # pagination page default
    page = 1
    # pagination default for page size.
    limit = 20
    # Boolean, when True each page of data will write a file with a page number
    chunk = False
    # Boolean, when True a list will not be kept in memory or
    # returned (None instead)
    less_memory = False

    """Extract collection type data"""

    def __init__(self, creds=None, verbose=False):
        """
        Call the super, our toilet is clogged.
        :return:
        """
        super(ExtractCollectionData, self).__init__(creds, verbose)

    def extract_custom_collection_data(self, write=True):
        """
        Map all custom collection
        :param write: bool, optional, default True (write to /json folder)
        :return: list on success or None on fail (writes to self.errors)
        """
        # determine how many Custom Collections are in the System
        call = 'admin/custom_collections/count.json'
        res = self.shopify_get(call)  # {u'count': 5}
        if res is None:
            self.errors.append('calling %s returned None' % call)
            return False

        page = self.page
        limit = self.limit
        collection_starting_count = res.get('count', None)
        collection_results = []
        logging.info('\nBeginning Custom Collection Extraction')
        while page:
            logging.info('\n------Page: %s via limit %s', page, limit)
            call = 'admin/custom_collections.json?page=%s&limit=%s'
            call = call % (page, limit)
            res = self.shopify_get(call)
            if res is None:
                self.errors.append('The call [%s] returned None.' % call)
                break
            this_page = res.get('custom_collections', False)
            if'custom_collections' not in res or not this_page:
                page = None
            else:
                if self.chunk and write:
                    write_json(
                        this_page,
                        'extract_custom_collection_page_%s' % page,
                        overwrite_files=self.creds.overwrite_files
                    )
                # {u'custom_collections': []} is the return for no results
                if not self.less_memory:
                    collection_results += this_page
                page += 1
                logging.info('Sleeping for %s', self.sleep_interval)
                sleep(self.sleep_interval)

        logging.info('\nEnd Custom Collection Extraction')

        if self.errors:
            logging.info('\nCustom Collection Extraction has errors')
            return None

        if collection_starting_count != len(collection_results):
            msg = (
                'Collection starting count (%s) != number of results'
                ' pulled from the API (%s).'
            ) % (
                collection_starting_count,
                len(collection_results),
            )
            logging.warning(msg)
            self.errors.append(msg)
            return None

        if write:
            write_json(
                collection_results,
                'custom_collection',
                overwrite_files=self.creds.overwrite_files
            )

        logging.info(
            'Job complete: %s Custom Collections found', len(
                collection_results
            )
        )
        return collection_results

    def extract_smart_collection_data(self, write=True):
        """
        Map all smart collection
        :param write: bool, optional, default True (write to /json folder)
        :return: list on success or None on fail (writes to self.errors)
        """
        # get count fo smart collections
        call = 'admin/smart_collections/count.json'
        res = self.shopify_get(call)
        if res is None:
            self.errors.append('calling %s returned None' % call)
            return False
        collection_starting_count = res.get('count', None)

        page = self.page
        limit = self.limit
        collection_results = []
        logging.info('\nBeginning Smart Collection Extraction')
        while page:
            logging.info('\n------Page: %s via limit %s', page, limit)
            call = 'admin/smart_collections.json?page=%s&limit=%s'
            call = call % (page, limit)
            res = self.shopify_get(call)
            if res is None:
                self.errors.append('The call [%s] returned None.' % call)
                break
            this_page = res.get('smart_collections', False)
            if'smart_collections' not in res or not this_page:
                page = None
            else:
                if self.chunk and write:
                    write_json(
                        this_page,
                        'extract_custom_collection_page_%s' % page,
                        overwrite_files=self.creds.overwrite_files
                    )
                # {u'custom_collections': []} is the return for no results
                if not self.less_memory:
                    collection_results += this_page
                page += 1
                logging.info('Sleeping for %s', self.sleep_interval)
                sleep(self.sleep_interval)

        logging.info('\nEnd Smart Collection Extraction')

        if self.errors:
            logging.info('\nSmart Collection Extraction has errors')
            return None

        if collection_starting_count != len(collection_results):
            msg = (
                'Collection starting count (%s) != number of results '
                'pulled from the API (%s).'
            ) % (
                collection_starting_count,
                len(collection_results),
            )
            logging.warn(msg)
            self.errors.append(msg)
            return None

        if write:
            write_json(
                collection_results,
                'smart_collection',
                overwrite_files=self.creds.overwrite_files
            )

        logging.info(
            'Job complete: %s Smart Collections found', len(
                collection_results
            )
        )
        return collection_results

    def extract_collect_data(self, write=True):
        """
        Map all smart collection
        :param write: bool, optional, default True (write to /json folder)
        :return: list on success or None on fail (writes to self.errors)
        """
        # get count fo smart collections
        call = 'admin/collects/count.json'
        res = self.shopify_get(call)
        if res is None:
            self.errors.append('calling %s returned None' % call)
            return False
        collection_starting_count = res.get('count', None)

        page = self.page
        limit = self.limit
        collection_results = []
        logging.info('\nBeginning Collect Extraction')
        while page:
            logging.info('\n------Page: %s via limit %s', page, limit)
            call = 'admin/collects.json?page=%s&limit=%s'
            call = call % (page, limit)
            res = self.shopify_get(call)
            if res is None:
                self.errors.append('The call [%s] returned None.' % call)
                break
            this_page = res.get('collects', False)
            if'collects' not in res or not this_page:
                page = None
            else:
                if self.chunk and write:
                    write_json(
                        this_page,
                        'extract_custom_collection_page_%s' % page,
                        overwrite_files=self.creds.overwrite_files
                    )
                # {u'custom_collections': []} is the return for no results
                if not self.less_memory:
                    collection_results += this_page
                page += 1
                logging.info('Sleeping for %s', self.sleep_interval)
                sleep(self.sleep_interval)

        logging.info('\nEnd Collect Extraction')

        if self.errors:
            logging.info('\nCustom Collect has errors')
            return None

        if collection_starting_count != len(collection_results):
            msg = 'Collection starting count (%s) != number of results pulled ' \
                'from the API (%s).' % (
                    collection_starting_count,
                    len(collection_results),
                )
            logging.warn(msg)
            self.errors.append(msg)
            return None

        if write:
            write_json(
                collection_results,
                'collect',
                overwrite_files=self.creds.overwrite_files
            )

        logging.info(
            'Job complete: %s Collect (relationships) found', len(
                collection_results
            )
        )
        return collection_results

    # -----------
    # Overrides |
    # -----------

    def shopify_delete(self, call):
        """
        Override destructive method
        :param call:
        :return:
        """
        logging.error('shopify_delete called and forbidden')
        pass

    def shopify_put(self, call, data=None, headers=None):
        """
        Override destructive method
        :param call:
        :param data:
        :param headers:
        :return:
        """
        logging.error('shopify_put called and forbidden')
        pass

    def shopify_post(self, call, data=None, headers=None):
        """
        Override destructive method
        :param call:
        :param data:
        :param headers:
        :return:
        """
        logging.error('shopify_post called and forbidden')
        pass


