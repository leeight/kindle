#!/usr/bin/env python
#!-*- coding:utf-8 -*-
#!vim: set ts=4 sw=4 sts=4 tw=100 noet:
# ***************************************************************************
# 
# Copyright (c) 2012 Baidu.com, Inc. All Rights Reserved
# $Id$ 
# 接收请求，放到message queue里面去
# **************************************************************************/



import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler


__author__ = 'leeight <liyubei@baidu.com>'
__date__ = '2012/06/09 20:21:29'
__revision = '$Revision$'

import tornado.ioloop
import tornado.web
import redis
import json

class SendToKindleHandler(tornado.web.RequestHandler):
  def get(self):
    self.set_header("Content-Type", "text/javascript; charset=utf-8")

    email = self.get_argument("email")
    title = self.get_argument("title")
    url = self.get_argument("url")
    version = self.get_argument("version", default="6")
    callback = self.get_argument("callback", default="callback")

    try:
      server = redis.Redis("localhost")
      mq_length = server.lpush("MQ_SEND_TO_KINDLE", json.dumps((email, title, url, version)))
      logging.debug('mq_length = [%d]', mq_length)
      self.write("%s(%s);" % (callback, json.dumps({
          "success" : True,
          "mq_length" : mq_length
      })))
    except:
      self.write("%s(%s);" % (callback, json.dumps({
          "success" : False,
          "message" : "redis server was down"
      })))

class FaviconHandler(tornado.web.RequestHandler):
  def get(self):
    self.redirect("http://www.baidu.com/favicon.ico", True)

class ClearMQHandler(tornado.web.RequestHandler):
  def get(self):
    try:
      count = 0
      server = redis.Redis("localhost")
      while server.llen("MQ_SEND_TO_KINDLE"):
        server.brpop("MQ_SEND_TO_KINDLE")
        count += 1
      self.write("clear %s items" % count)
    except:
      pass

application = tornado.web.Application([
  (r"/send_to_kindle", SendToKindleHandler),
  (r"/clear_mq", ClearMQHandler),
  (r"/favicon\.ico", FaviconHandler)
])

if __name__ == "__main__":
  logger = logging.getLogger()
  logger.addHandler(TimedRotatingFileHandler("logs/access.log"))
  logger.setLevel(-1)

  application.listen(8965)
  tornado.ioloop.IOLoop.instance().start()

