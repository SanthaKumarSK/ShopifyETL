#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Basic implementation"""

from __future__ import print_function
import logging
import os
from shopify_creds import ShopifyCreds
from jobs.collections import ExtractCollectionData
from jobs.products import ExtractProducts

# let's get noisy
logging.basicConfig(level=logging.INFO)  # global
logger = logging.getLogger()
fh = logging.FileHandler('%s/transform_log.txt' % os.path.dirname(os.path.realpath(__file__)))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


if __name__ == "__main__":

    # ----------------------
    # Run basic extraction |
    logging.info('Beginning extraction via run.py')
    col = ExtractCollectionData(ShopifyCreds())
    logging.info('Start Smart Collections')
    smart_collections = col.extract_smart_collection_data()
    logging.info('Start Custom Collections')
    custom_collections = col.extract_custom_collection_data()
    logging.info('Start Collects')
    collect_data = col.extract_collect_data()

    logging.info('Start Products')
    pro = ExtractProducts(ShopifyCreds())
    product_data_all = pro.extract_product()

    logging.info('Complete')

    # --------------------
    # # Chunk everything |
    # logging.info('Beginning extraction via run.py')
    # col = ExtractCollectionData(ShopifyCreds())
    # col.chunk = True
    # # col.limit = 1  # 1 item per page, good for testing otherwise a bad idea
    # logging.info('Start Smart Collections')
    # smart_collections = col.extract_smart_collection_data()
    # logging.info('Start Custom Collections')
    # custom_collections = col.extract_custom_collection_data()
    # logging.info('Start Collects')
    # collect_data = col.extract_collect_data()
    #
    # logging.info('Start Products')
    # pro = ExtractProducts(ShopifyCreds())
    # pro.chunk = True
    # product_data_all = pro.extract_product()
    #
    # logging.info('Complete')

    # ----------------
    # Reduced memory |
    # col = ExtractCollectionData(ShopifyCreds())
    # col.less_memory = True
    # # col.limit = 1  # 1 item per page, good for testing otherwise a bad idea
    # smart_collections = col.extract_smart_collection_data()
    # print(smart_collections)
    # # ERROR:root:Collection starting count (15) != number of results pulled from the API (0).


