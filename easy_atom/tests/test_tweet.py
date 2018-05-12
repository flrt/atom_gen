#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    test simple de l'action mail
"""

import os.path
import unittest
import logging
import datetime

from easy_atom import action, helpers


class TestTweet(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger('tests')

    def test_tweet_conf(self):
        self.logger.info("test_tweet_conf")
        conffn = 'myconf/twitter.json'

        self.assertTrue(os.path.exists(conffn))

        act = action.TweetAction(conf_filename=conffn)
        self.logger.info(act.conf)

        self.assertTrue('consumer_key' in act.conf)
        self.assertTrue('consumer_secret' in act.conf)
        self.assertTrue('access_token' in act.conf)
        self.assertTrue('access_token_secret' in act.conf)

    def test_tweet(self):
        self.logger.info("test_tweet")
        conffn = 'myconf/twitter.json'

        self.assertTrue(os.path.exists(conffn))

        act = action.TweetAction(conf_filename=conffn)
        n = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        ret = act.process("Test - Unit test (now {})".format(n))
        self.logger.info("Id : {}".format(ret))
        
        self.assertIsNotNone(ret)

    def test_tweet_error(self):
        self.logger.info("test_tweet_error")
        conffn = 'myconf/twitter.json'

        self.assertTrue(os.path.exists(conffn))

        act = action.TweetAction(conf_filename=conffn)
        ret1 = act.process("Test - Unit test")
        self.logger.info("Id 1 : {}".format(ret1))
        ret2 = act.process("Test - Unit test")

        self.assertIsNone(ret2)


if __name__ == '__main__':
    loggers = helpers.stdout_logger(['tests','action'], logging.DEBUG)
    unittest.main()
