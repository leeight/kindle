#!/usr/bin/env python
#!-*- coding:utf-8 -*-
#!vim: set ts=4 sw=4 sts=4 tw=100 noet:
# ***************************************************************************
#
# Copyright (c) 2012 Baidu.com, Inc. All Rights Reserved
# $Id$
# 从消息队列里面获取任务，依次处理
# **************************************************************************/



import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
import redis
import subprocess
import json
from os.path import dirname, join

__author__ = 'leeight <liyubei@baidu.com>'
__date__ = '2012/06/10 08:54:08'
__revision = '$Revision$'

KINDLE_CSS_TPL = open(join(dirname(__file__), 'kindle.css')).read()

def utf8(s):
  if isinstance(s, unicode):
    return s.encode("utf-8")
  assert isinstance(s, str)
  return s

def send_mail(receiver, subject, attachment):
  import smtplib
  from email.MIMEMultipart import MIMEMultipart
  from email.MIMEBase import MIMEBase
  from email import Encoders

  sender = "adocnoreply@gmail.com"

  msg = MIMEMultipart()
  msg['Subject'] = utf8(subject)
  msg['From'] = sender
  msg['To'] = receiver

  if os.path.exists(attachment):
    part = MIMEBase('application', "pdf")
    part.set_payload(open(attachment, "rb").read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="' +
        os.path.basename(attachment) + '"')
    msg.attach(part)

  session = smtplib.SMTP('smtp.gmail.com', 587)
  session.ehlo()
  session.starttls()
  session.login(sender, "MhxzKhl262")
  session.sendmail(sender, receiver, msg.as_string())
  session.quit()
  logging.debug("send to [%s]", receiver)

def fetch_as_attachment(title, url, version = 6):
  import tempfile

  f = tempfile.NamedTemporaryFile(delete=True, suffix='.css')
  f.write(KINDLE_CSS_TPL.replace("[SDCFE]新人指南-feutils",
      "[ADoc]" + utf8(title)))
  f.flush()

  dest_pdf = utf8(title) + '.pdf'

  args = ['prince', utf8(url), '-s', f.name, '-o', dest_pdf]
  logging.debug(' '.join(args))

  proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  (stdoutdata, stderrdata) = proc.communicate()
  if proc.returncode != 0:
    logging.error('fetch_as_attachment failed.')
    logging.error('\n' + stderrdata)
    return None
  else:
    if stderrdata:
      logging.warning(stderrdata)
    return dest_pdf

def main():
  server = redis.Redis("localhost")
  while True:
    try:
      key, _ = server.brpop("MQ_SEND_TO_KINDLE")
      item = json.loads(_)
      email, title, url, version = item[0], item[1], item[2], item[3]
      logging.debug("email = [%s], title = [%s], url = [%s], version = [%s]",
          email, title, url, version)
      attachment = fetch_as_attachment(title, url, version)
      send_mail(email, title, attachment)
    except Exception as e:
      logging.error(e)
      import time
      time.sleep(1)

if __name__ == '__main__':
  logger = logging.getLogger()
  logger.addHandler(TimedRotatingFileHandler("logs/worker.log"))
  logger.setLevel(-1)

  main()





