#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Testing"""

from __future__ import print_function
import logging
import os
import unittest
import uuid
from util import ping_shop, strip_new_line, strip_multi_whitespace, write_json
from shopify import Shopify

# set logging level
logging.basicConfig(level=logging.DEBUG)

# ----------
# Fixtures |
# ----------

util_ping_shop_tests_true = [  # util.ping_shops(arg1, arg2)
    ('unit-testing-store', False, True),  # arg1, arg2, expected result
    ('unit-testing-store.myshopify.com', True, True),  # arg1, arg2, expected result
]
util_ping_shop_tests_false = [  # util.ping_shops(arg1, arg2)
    ('unit-testing-store-xoxoxoxoxoxoxoxoxoxox', False, False),  # arg1, arg2, expected result
    (
        'unit-testing-store-xoxoxoxoxoxoxoxoxoxox.myshopify.com',
        True,
        False
    ),  # arg1, arg2, expected result
]

triple_quote_1 = """a
b
c"""

strip_new_line_tests = [  # string, expected length
    ('abcdefg', 7),
    ('abc\ndefg', 7),
    (triple_quote_1, 3)
]

strip_multi_whitespace_tests = [
    ('abc', 3),  # string, expected length
    ('ab c', 4),
    ('ab  c', 4),
    (' ab  c', 5),
    (' ab  c', 5),
    ('  ab  c', 5),
    ('  ab  c ', 6),
    ('  ab  c  ', 6),
    (' ', 1),
    ('  ', 1),
    ('   ', 1),
]

prepare_call_tests = [
    ('admin/shop.json', 15),  # string, expected length
    ('/admin/shop.json', 15),
    ('/admin/shop.json/', 15),
    ('/admin/shop.json\\', 15),
    ('\\admin/shop.json\\', 15),
]


class TestUtil(unittest.TestCase):

    """util tests"""

    def test_ping_shop(self):
        """
        Test the ping_shop call
        :return:
        """
        for test in util_ping_shop_tests_true:
            self.assertTrue(ping_shop(test[0], test[1]))
        for test in util_ping_shop_tests_false:
            self.assertFalse(ping_shop(test[0], test[1]))

    def test_strip_new_line(self):
        """
        Test strip_new_line
        :return:
        """
        for payload, count in strip_new_line_tests:
            self.assertEqual(
                len(strip_new_line(payload)),
                count
            )

    def test_strip_multi_whitespace(self):
        """
        Test strip_multi_whitespace
        :return:
        """
        for payload, count in strip_multi_whitespace_tests:
            self.assertEqual(
                len(strip_multi_whitespace(payload)),
                count,
            )

    def test_basic_shopify_methods(self):
        """
        Non-connection tests
        :return:
        """
        fake_creds = dict(
            SHOPIFY_KEY='incorrect_value',
            SHOPIFY_PASSWORD='incorrect_value',
            SHOPIFY_STORE='incorrect_value',
            SHOPIFY_BASE_URL='incorrect_value',
        )
        s = Shopify(fake_creds)
        for call, count in prepare_call_tests:
            self.assertEqual(
                len(s.prepare_call(call)),
                count,
            )

    def test_write_json(self):
        """
        Test write_json() using list, dict, string w/cleanup
        :return:
        """
        teardown = []  # holds all of the files we should cleanup

        # count files in json
        loc = os.path.dirname(os.path.realpath(__file__)) + '/json'

        # -------------
        # Test 1 list |
        # -------------

        beginning_file_count = len(
            [name for name in os.listdir(loc) if os.path.isfile(
                os.path.join(
                    loc, name
                )
            )]
        )
        # write file name
        target_file = str(uuid.uuid4())
        # reminder --- no .json--^----v
        new_loc = write_json([], target_file)  # as list
        teardown.append(new_loc)
        # confirm writen
        self.assertTrue(os.path.isfile(new_loc))
        # try to write again
        new_loc = write_json([], target_file)  # as list
        teardown.append(new_loc)
        self.assertTrue(os.path.isfile(new_loc))
        # count files in json -- should be +2
        ending_file_count = len(
            [name for name in os.listdir(loc) if os.path.isfile(
                os.path.join(loc, name)
            )]
        )
        self.assertTrue(
            beginning_file_count+2 == ending_file_count,
            msg='File count expected to match beginning count+2'
        )

        # -----------------------------------------
        # Okay, now do it again testing on dict() |
        # -----------------------------------------
        # count files in json
        beginning_file_count = len(
            [name for name in os.listdir(loc) if os.path.isfile(
                os.path.join(loc, name)
            )]
        )
        # write file name
        target_file = str(uuid.uuid4())
        # reminder --- no .json--^----v
        new_loc = write_json([], target_file)  # as dict
        teardown.append(new_loc)
        # confirm writen
        self.assertTrue(os.path.isfile(new_loc))
        # try to write again
        new_loc = write_json({}, target_file)  # as dict
        teardown.append(new_loc)
        self.assertTrue(os.path.isfile(new_loc))

        # count files in json -- should be +2
        ending_file_count = len(
            [name for name in os.listdir(loc) if os.path.isfile(
                os.path.join(loc, name)
            )]
        )
        self.assertTrue(
            beginning_file_count+2 == ending_file_count,
            msg='File count expected to match beginning count+2'
        )

        # -----------------------------------------
        # Okay, now do it again testing on string |
        # -----------------------------------------

        # count files in json
        beginning_file_count = len(
            [name for name in os.listdir(loc) if os.path.isfile(
                os.path.join(
                    loc,
                    name
                )
            )]
        )
        # write file name
        target_file = str(uuid.uuid4())
        # reminder --- no .json--^----v
        new_loc = write_json([], target_file)  # as list
        teardown.append(new_loc)
        # confirm writen
        self.assertTrue(os.path.isfile(new_loc))
        # try to write again
        new_loc = write_json('{}', target_file)  # as list
        teardown.append(new_loc)
        self.assertTrue(os.path.isfile(new_loc))
        # count files in json -- should be +2
        ending_file_count = len(
            [name for name in os.listdir(loc) if os.path.isfile(
                os.path.join(loc, name)
            )]
        )
        self.assertTrue(
            beginning_file_count+2 == ending_file_count,
            msg='File count expected to match beginning count+2'
        )

        # -----------------------------------------------------------------
        # Okay, now do it again testing on string but w/extended recursion|
        # -----------------------------------------------------------------

        # count files in json
        beginning_file_count = len(
            [name for name in os.listdir(loc) if os.path.isfile(
                os.path.join(
                    loc,
                    name
                )
            )]
        )
        # write file name
        target_file = str(uuid.uuid4())
        # reminder --- no .json--^----v
        new_loc = write_json([], target_file)  # as list
        teardown.append(new_loc)
        # confirm writen
        self.assertTrue(os.path.isfile(new_loc))

        # try to write again
        new_loc = write_json('{}', target_file)  # as list
        teardown.append(new_loc)

        # try to write again again
        new_loc = write_json('{}', target_file+'_trace')  # as list
        teardown.append(new_loc)

        self.assertTrue(os.path.isfile(new_loc))
        # count files in json -- should be +2
        ending_file_count = len(
            [name for name in os.listdir(loc) if os.path.isfile(
                os.path.join(loc, name)
            )]
        )
        self.assertTrue(
            beginning_file_count+3 == ending_file_count,
            msg='File count expected to match beginning count+2'
        )

        # -------------------------------------------------------------
        # Okay, now do it again testing on string and allow overwrite |
        # -------------------------------------------------------------

        # count files in json
        beginning_file_count = len(
            [name for name in os.listdir(loc) if os.path.isfile(
                os.path.join(loc, name)
            )]
        )
        # write file name
        target_file = str(uuid.uuid4())
        # reminder --- no .json--^----v
        new_loc = write_json([], target_file, overwrite_files=True)  # as list
        teardown.append(new_loc)
        # confirm writen
        self.assertTrue(os.path.isfile(new_loc))
        # try to write again
        new_loc = write_json('{}', target_file, overwrite_files=True)  # as list
        # note: do not add new_loc a second time to the teardown!
        # count files in json -- should be +2
        ending_file_count = len(
            [name for name in os.listdir(loc) if os.path.isfile(
                os.path.join(loc, name)
            )]
        )
        self.assertTrue(
            beginning_file_count+1 == ending_file_count,
            msg='File count expected to match beginning count+1'
        )

        # teardown, clean up this fucking mess
        if teardown:
            for item in teardown:
                os.remove(item)
                self.assertFalse(os.path.isfile(item), msg='Failed to delete %s' % item)
        logging.info('\n> Teardown complete')

if __name__ == "__main__":
    unittest.main()
