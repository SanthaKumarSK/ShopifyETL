#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Shopify Base Class"""

from __future__ import print_function
import requests
import logging
import json


def handle_429(calltype, call, data=None, params=None):
    """
    Custom handler for Shopify 429 https://docs.shopify.com/api/guides/api-call-limit
    :param calltype: required post/get/etc
    :param call: required, string representing the appended call path
    :param data: optional data sent ot call
    :param params: optional params sent to call
    :return: void
    Sends admin emails
    """
    message = 'Error 429 returned for "%s" call %s \n using data %s\n and params %s.' % (
        calltype, call, data, params
    )
    logging.warn('> 429 Error detected! here is the message sent to admins: %s', message)


class Shopify(object):

    """Base Shopify Class"""

    base = 'https://%s:%s@%s.myshopify.com/'  # key / pass / store
    # overwrite_files = False  # flag used by write_json()

    def __init__(self, creds_object, verbose=False):
        """
        From nothing create something.
        :param creds: dict, required, cred object
        :param verbose: Is additional logging printed (rather noisy)
        :return:
        """
        self.verbose = verbose  # logging on/off
        self.creds = creds_object
        self.conn = None
        self.errors = []

    def get_connection(self):
        """
        Create the base connection string ready for a call
        :return:
        """
        if self.conn is None:
            self.conn = self.base % (
                self.creds.SHOPIFY_KEY,
                self.creds.SHOPIFY_PASSWORD,
                self.creds.SHOPIFY_STORE
            ) + '%s'
        return self.conn

    def shopify_get(self, call, params=None):
        """
        Make a get call to Shopify
        :param call:
        :param params:
        :return: None or data for product (request.contents)
        """
        call = self.prepare_call(call)
        if params is not None:
            req = requests.get(self.get_connection() % call, params=params)
        else:
            req = requests.get(self.get_connection() % call)
        if req.status_code == 429:
            handle_429(
                'get', call, params=params
            )
        if req.status_code != 200 and req.status_code != 201:  # do we get 201 here also?
            if self.verbose:
                logging.error('>>bad status using shopify_get(): %s', req.status_code)
                logging.error('> r.request %s', req.request)
                logging.error('> r.content %s', req.content)
                logging.error('> r.raw %s', req.raw)
                logging.error('> r.text %s', req.text)
            return None
        else:
            return json.loads(req.content)

    def shopify_post(self, call, data=None, headers=None):
        """
        Make a post call to Shopify
        :param call: strong, required, API path
        :param data: strong, required, json data
        :param headers: optional dict of headers
        :return: return strong, should be json
        ** Note: no leading slash
        """
        call = self.prepare_call(call)
        if headers is None:
            headers = {'Content-Type': 'application/json'}
        if data is not None:
            req = requests.post(self.get_connection() % call, headers=headers, data=data)
        else:
            req = requests.post(self.get_connection() % call, headers=headers)
        if req.status_code == 429:
            handle_429('post', call, data=data)
        if req.status_code != 200 and req.status_code != 201:
            if self.verbose:
                logging.error('>>bad status using shopify_post(): %s', req.status_code)
                logging.error('> r.request %s', req.request)
                logging.error('> r.content %s', req.content)
                logging.error('> r.raw %s', req.raw)
                logging.error('> r.text %s', req.text)
            return None
        else:
            return json.loads(req.content)

    def shopify_put(self, call, data=None, headers=None):
        """
        Make a put call to Shopify
        :param call: path on api
        :param data: data, json
        :param headers: optional
        :return: content, none on error

        # /admin/custom_collections/841564295.json   PUT
        # requests.put(url, data=None, **kwargs)

        """
        call = self.prepare_call(call)
        if headers is None:
            headers = {'Content-Type': 'application/json'}
        if data is not None:
            req = requests.put(self.get_connection() % call, headers=headers, data=data)
        else:
            req = requests.put(self.get_connection() % call, headers=headers)
        if req.status_code == 429:
            handle_429('post', call, data=data)
        if req.status_code != 200 and req.status_code != 201:
            if self.verbose:
                logging.error('>>bad status using shopify_put(): %s', req.status_code)
                logging.error('> r.request %s', req.request)
                logging.error('> r.content %s', req.content)
                logging.error('> r.raw %s', req.raw)
                logging.error('> r.text %s', req.text)
            return None
        else:
            return json.loads(req.content)

    def shopify_delete(self, call):
        """
        Make a delete call to Shopify
        :param call: path on api
        :return: content, none on error
        """
        call = self.prepare_call(call)
        req = requests.delete(self.get_connection() % call)
        if req.status_code == 429:
            handle_429('post', call, data=None)
        if req.status_code != 200 and req.status_code != 201:
            if self.verbose:
                logging.error('>>bad status using shopify_delete(): %s', req.status_code)
                logging.error('> r.request %s', req.request)
                logging.error('> r.content %s', req.content)
                logging.error('> r.raw %s', req.raw)
                logging.error('> r.text %s', req.text)
            return None
        else:
            return json.loads(req.content)

    @classmethod
    def prepare_call(cls, call):
        """
        Prepare the call for this module.
        :param call:
        :return: string (call)
        """
        # Could be a while loop and combat multiple trailing/leading slashes.
        # But we can only spend time protecting to a certain level of stupidity
        if call[-1:] == '/' or call[-1:] == '\\':  # trim leading slashes
            call = call[:-1]
        if call[:1] == '/' or call[:1] == '\\':  # trim trailing slashes
            call = call[1:]
        return call
