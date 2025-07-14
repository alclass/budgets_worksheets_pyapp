#!/usr/bin/env python3
"""
fs/textfs/logfunctions.py
"""
import datetime
import logging
import os
import settings as sett
_, modlevelogfn = os.path.split(__file__)
modlevelogfn = str(datetime.date.today()) + '_' + modlevelogfn[:-3] + '.log'
modlevelogfp = os.path.join(sett.get_datafolder_abspath(), modlevelogfn)
logging.basicConfig(filename=modlevelogfp, filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # DEBUG means it and all others levels will be logged


def log_error_namedtuple(named_tuple):
  log_msg = 'Error named_tuple ' + str(named_tuple)
  logger.info(log_msg)
  print(log_msg)
  try:
    print(named_tuple.error_msg)
  except AttributeError:
    pass
  return named_tuple
