#!/usr/bin/env python
#!-*- coding:utf-8 -*-
#!vim: set ts=4 sw=4 sts=4 tw=100 noet:
# ***************************************************************************
# 
# Copyright (c) 2012 Baidu.com, Inc. All Rights Reserved
# $Id$ 
# 
# **************************************************************************/
 
 
 
import os
import sys
import unittest
import worker
import logging
 
 
__author__ = 'leeight <liyubei@baidu.com>'
__date__ = '2012/06/10 13:40:50'
__revision = '$Revision$'

class WorkerTestCase(unittest.TestCase):
  def testSendmail(self):
    worker.send_mail("leeight@gmail.com", "我很好啊", "feutils.pdf")
    pass




if __name__ == '__main__':
  logging.basicConfig(format="%(asctime)-15s %(levelname)-5s %(message)s", level=logging.DEBUG)
  unittest.main()
