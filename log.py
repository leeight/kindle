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
import logging
from logging.handlers import TimedRotatingFileHandler


__author__ = 'leeight <liyubei@baidu.com>'
__date__ = '2012/06/10 14:16:21'
__revision = '$Revision$'


def init_log(log_path):
  formatter = logging.Formatter('%(asctime)-15s - %(levelname)s - %(message)s')

  handler = TimedRotatingFileHandler(log_path)
  handler.setFormatter(formatter)

  logger = logging.getLogger()
  logger.addHandler(handler)
  logger.setLevel(-1)



