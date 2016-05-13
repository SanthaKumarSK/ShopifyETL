#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract products"""

from __future__ import print_function
from time import sleep
import logging
from shopify import Shopify
from util import write_json


class ExtractProducts(Shopify):

    """Extract products"""

    # int for seconds between page calls
    sleep_interval = 1
    # pagination page default
    page = 1
    # pagination default for page size.
    limit = 20
    # Boolean, when True each page of data will write a file with a page number
    chunk = False
    # Boolean, when True a list will not be kept in memory or returned (None instead)
    less_memory = False

    def __init__(self, creds=None, verbose=False):
        """
        Call the super, Zuul is being loud again.
        :return:
        """
        super(ExtractProducts, self).__init__(creds, verbose)

    def extract_product(self, write=True):
        """
        Extract all of the products
        :param write: bool, optional, default True. Flag for writing to the local file system
        :return: list or None on fail+writes to errors
        """
        # determine how many Custom Collections are in the System
        call = 'admin/products/count.json'
        res = self.shopify_get(call)
        if res is None:
            self.errors.append('calling %s returned None' % call)
            return False
        product_starting_count = res.get('count', None)

        # get all of the collection info
        page = self.page
        limit = self.limit
        product_results = []
        product_count = 0
        logging.info('\nBeginning Product [all] Extraction')
        while page:
            logging.info('\n------Page: %s via limit %s', page, limit)
            call = 'admin/products.json?page=%s&limit=%s'
            call = call % (page, limit)
            res = self.shopify_get(call)
            if res is None:
                self.errors.append('The call [%s] returned None.' % call)
                break
            this_page = res.get('products', False)
            if'products' not in res or not this_page:
                page = None
            else:
                # {u'custom_collections': []} is the return for no results
                if not self.less_memory:
                    product_results += this_page

                if self.chunk and write:
                    write_json(
                        this_page,
                        'products_all_page_%s' % page,
                        overwrite_files=self.creds.overwrite_files
                    )

                page += 1
                product_count += len(this_page)
                logging.info('Sleeping for %s', self.sleep_interval)
                sleep(self.sleep_interval)

        logging.info('\nEnd Product [all] Extraction')

        if self.errors:
            logging.info('\nProduct [all] Extraction has errors')
            return None

        if product_starting_count != product_count:
            msg = 'Product starting count (%s) != number of results pulled from the API (%s).' % (
                product_starting_count,
                len(product_results),
            )
            logging.error(msg)
            self.errors.append(msg)
            return None

        if write:
            write_json(product_results, 'products_all', overwrite_files=self.creds.overwrite_files)

        logging.info(
            'Job complete: %s Products (all) found', len(
                product_results
            )
        )
        return product_results

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
