"""
adhoctests/dateadhoctests/text_with_different_date_formats_adhoctest.py
"""
import os
import fs.datefs.years_date_functions as dtfs
import settings as sett
DEFAULT_TXT_DATES_FILENAME = 'datesfile.txt'


def get_default_datesfile():
  folderpath = sett.get_datafolder_abspath()
  filename = DEFAULT_TXT_DATES_FILENAME
  filepath = os.path.join(folderpath, filename)
  return filepath


def get_datesfile(filepath=None):
  if filepath is None:
    return get_default_datesfile()
  if filepath.find(os.sep) < 0:
    folderpath = sett.get_datafolder_abspath()
    filename = filepath
    filepath = os.path.join(folderpath, filename)
  if not os.path.isfile(filepath):
    error_msg = 'File does not exist [%s].' % str(filepath)
    raise OSError(error_msg)
  return filepath


def fetch_dates_from_datesfile(filepath=None):
  if filepath is None or not os.path.isfile(filepath):
    return []
  text = open(filepath).read()
  lines = text.split('\n')
  strdatelist = []
  for line in lines:
    words = line.split(' ')
    words = list(map(lambda e: e.strip('\t\r\n'), words))
    # notice that words itself is an iterable/list, so the list-comprehension below
    # will help pick up the elment(s) to be appended to strdatelist
    _ = [strdatelist.append(word) for word in words]
  # notice that dates may be in some different formats (eg "2021-01-21" or "21/1/2021")
  # but they must all be converted to type datetime.date
  return strdatelist


def convert_strdates_to_dates(strdates):
  """
  TO CORRECT:
    The algorithm must first decide, for the whole input list, the "position-format",
    then process the whole list with that found format

    The problem we got now is that all dates with day less than 13
      (confusing to the inconclusive hypothesis ie when both day and month are less than 13)
    The algorithm must find at least 'one sample' in the 'population'.
    Of course, if all dates are inconclusive, an exception should be raised and allow the user
      to enter a config date-format before hand.
  """
  datelist = dtfs.introspect_n_convert_strdatelist_to_dates(strdates)
  datelist = sorted(filter(lambda e: e is not None, datelist))
  return sorted(datelist)


def adhoctest():
  filepath = get_datesfile()
  strdates = fetch_dates_from_datesfile(filepath)
  dates = convert_strdates_to_dates(strdates)
  for i, pdate in enumerate(dates):
    strdate = strdates[i]
    print(i+1, strdate, '=>', pdate)


if __name__ == "__main__":
  """
  process()
  """
  adhoctest()
