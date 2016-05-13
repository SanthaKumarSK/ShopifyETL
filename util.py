import logging
import re
import os
import json
# Try used as a firewall to allow other scripts to complete without the package shitting a brick
try:
    import requests
except ImportError:
    logging.error('ImportError for requests in util')


"""Whole bunch of utilities"""


def ping_shop(shop, fqdn=False):
    """
    Make simple request ot shop and look for 2xx response
    :param shop: string, the shop name defined in the config
    :param fqdn: string, optional, if set will espect a FQDN incli HTTP(s)
    :return: bool
    """
    if fqdn:
        shop = 'https://%s' % shop
    else:
        shop = 'https://%s.myshopify.com' % shop
    try:
        logging.info('Making request to %s' % shop)
        r = requests.get(shop)
        if not unicode(r.status_code).startswith('2'):
            logging.error('The request to %s did not return a 2xx status code.' % shop)
            return False
        return True
    except requests.exceptions.ConnectionError as e:
        logging.error('Requests moduile raised a ConnectionError error when trying to call %s' % shop)
        logging.error('Exception: %s' % e)
        return False


def strip_new_line(str_json):
    """
    Strip \n new line
    :param str_json: string
    :return: string
    """
    str_json = str_json.replace('\n', '')  # kill new line breaks caused by triple quoted raw strings
    return str_json


def strip_multi_whitespace(str_json):
    """
    strip multi white space like "   " to a single  " "
    :param str_json: string
    :return: string
    """
    str_json = re.sub(' +', ' ', str_json)  # kills multi whitespace
    return str_json


def write_json(data, file_name, overwrite_files=False, prepend_count=1):
    """
    Handy and/or dandy function to write data to a static file in the module.
    :param data: dist/list/string, required, the data to write
    :param file_name:
    :param overwrite_files:
    :param prepend_count:
    :return:
    """
    # validate location
    json_dir = os.path.dirname(os.path.realpath(__file__))+'/json'

    if not os.path.isdir(json_dir):
        logging.error('Expected %s to be a valid dir.' % json_dir)
        return False
    # loc of the file to be written
    json_dir_template = '/'.join(
        [
            json_dir,
            '%s.json'
        ]
    )

    # create file path/name
    target_file_path = json_dir_template % file_name

    if not overwrite_files:  # will need to rename on collision
        if os.path.isfile(target_file_path):
            # try using the prepend before we recurse
            target_file_path = json_dir_template % '%s_%s' % (file_name, prepend_count)
            if os.path.isfile(target_file_path):
                # okay, now we recurse
                prepend_count += 1
                write_json(
                    data,
                    file_name,
                    overwrite_files,
                    prepend_count,
                )

    data_file = open(target_file_path, "w")
    json_write = None
    if isinstance(data, list) or isinstance(data, dict):
        json_write = json.dumps(data)
    elif isinstance(data, str):
        # assumes ready to write, not judging
        json_write = data
    try:
        data_file.write(json_write)
    # Handles instance of None gracefully
    except TypeError as e:
        logging.error(e)
        logging.error('\n\n json write data:')
        logging.error(json_write)
        logging.error('\n\ndata:')
        logging.error(data)
        # because we care
        data_file.close()
        return None
    data_file.close()
    return target_file_path
