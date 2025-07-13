#!/usr/bin/env python3
"""
fs/datefs/read_write_datelist_files_fs.py
"""
import datetime
import fs.datefs.convert_to_datetime_wo_intr_sep_posorder as dtfs
import os
# from urllib3.contrib.pyopenssl import orig_util_SSLContext
import fs.os.sufix_incrementor as sfx_incr
import fs.datefs.introspect_dates as intr  # .convert_strdate_to_date_or_none_w_sep_n_order
import fs.datefs.convert_to_date_wo_intr_sep_posorder as cnv  # .convert_str_or_attrsobj_to_date_or_none
import settings as sett
DEFAULT_DATE_SEPARATOR = '-'
DEFAULT_DATE_POSORDER = 'ymd'
DEFAULT_TXT_INPUT_DATES_FILENAME = 'datesfile.txt'
DEFAULT_TXT_OUTPUT_DATES_FILENAME = 'datesfile_processed_to_norm_yyyy-mm-dd.txt'


def make_new_sufixed_yyyy_mm_dd_fp_in_configdatafolder_giving_fn(
    infilename,
    p_datafolder_abspath=None,
    p_date=None
  ):
  """
  Makes and returns a file abspath equivalent to the input filename sufixed with a
   date in the yyyy-mm-dd format and located in the config data folder

  Example:
    suppose:
      filename = 'testfile.txt'
      configfolderpath = '/full/path'
    Then, the return result will be:
      "/full/path/testfile_20250626.txt"
      or, if filename is already taken,
      "/full/path/testfile_20250626_<n>.txt" when <n> represents a sequencial number 1, 2, 3...
  """
  if p_datafolder_abspath is None or not os.path.isdir(p_datafolder_abspath):
    datafolder_abspath = sett.get_datafolder_abspath()
  else:
    datafolder_abspath = p_datafolder_abspath
  indate = dtfs.convert_datetime_to_date_or_none(p_date)
  if indate is None:
    indate = datetime.date.today()
  name, dot_ext = os.path.splitext(infilename)
  outfilename = f"{name}{indate}{dot_ext}"
  outfilepath = os.path.join(datafolder_abspath, outfilename)
  i_iter, max_iter = 0, 1000
  while os.path.isfile(outfilepath):
    i_iter += 1
    if i_iter > max_iter:
      errmsg = f"""i_iter={i_iter} > max_iter={max_iter} in trying to make
       filepath [{outfilepath}] with date yyyymmdd stamp
        Please, delete or move files out of datafolder and retry.
        datafolder = [{datafolder_abspath}]"""
      raise ValueError(errmsg)
    outfilename = f"{name}{indate}_{i_iter}{dot_ext}"
    outfilepath = os.path.join(datafolder_abspath, outfilename)
  return outfilepath


def make_new_datetimestampsufix_fp_in_configdatafolder_giving_fn(infilename):
  """
  Makes and returns a file abspath where input filename is sufixed with a timestamp
  Makes and returns a file abspath equivalent to the input filename sufixed with a
   datetime stamp in the yyyymmddThhmmss format and located in the config data folder

  Example:
    suppose:
      filename = 'testfile.txt'
      conffolderpath = '/full/path'
    Then, the returned result will be:
      "/full/path/testfile_20250626T204817.txt"
  """
  strdt = make_tstamp_for_filename()
  name, dot_ext = os.path.splitext(infilename)
  if name.find(' ') > -1:
    outfilename = f"{name}{strdt}{dot_ext}"
    outfilename.replace('  ', ' ')
  else:
    outfilename = f"{name}_{strdt}{dot_ext}"
  datafolder_abspath = sett.get_datafolder_abspath()
  filepath = os.path.join(datafolder_abspath, outfilename)
  return filepath


def fetch_iter_wordlist_from_textfile_w_filepath(p_filepath=None):
  """
  Gets via iteration (yielding one by one) each first non-empty word of the lines of a text file
  """
  if p_filepath is None or not os.path.isfile(p_filepath):
    filepath = form_datesfilepath_w_folderpath_n_filename()
  else:
    filepath = p_filepath
  fd = open(filepath, 'r')
  line = fd.readline()
  while line:
    try:
      line = line.lstrip().rstrip()
      pp = line.split(' ')
      words = list(filter(lambda w: w != '', pp))
      if len(words) > 0:
        word = words[0]
        yield word
    except (IndexError, ValueError):
      pass
    line = fd.readline()
  return


def fetch_wordlist_from_textfile_w_filepath(p_filepath=None):
  """
  gets a list of words from the text inside filepath
  """
  if p_filepath is None or not os.path.isfile(p_filepath):
    filepath = form_datesfilepath_w_folderpath_n_filename()
  else:
    filepath = p_filepath
  text = open(filepath).read()
  lines = text.split('\n')
  strdatelist = []
  for line in lines:
    words = line.split(' ')
    words = list(map(lambda e: e.strip('\t\r\n'), words))
    # notice that words itself is an iterable/list, so the list-comprehension below
    # will help pick up the elment(s) to be appended to strdatelist
    _ = [strdatelist.append(word) if word != '' else word for word in words]
  # while '' in strdatelist:
  #   strdatelist.remove('')
  return strdatelist


def fetch_basic_yyyymmdd_dates_from_textfile_w_path(p_filepath=None):
  """
  The date introspected here is the one from make_date_or_none(),
    ie, dates are expected to be yyyy-mm-dd

  @see next function fetch_dates_from_strdates_in_text_wo_sep_but_of_oneform_from_filepath()
    for a routine that is capable of introspecting dates
      finding field-separator (/, - or .) and position (day, month, year) if possible
  """
  if p_filepath is None or not os.path.isfile(p_filepath):
    filepath = form_datesfilepath_w_folderpath_n_filename()
  else:
    filepath = p_filepath
  text = open(filepath).read()
  dates = text.split('\n')
  dates = map(lambda e: e.strip('\t\r\n'), dates)
  dates = filter(lambda e: e != '', dates)
  dates = map(lambda e: intr.make_date_or_none(e), dates)
  dates = filter(lambda e: e is not None, dates)
  dates = sorted(set(dates))
  return dates


def fetch_dates_from_strdates_in_text_wo_sep_but_of_oneform_from_filepath(filepath=None):
  """
  strdates with sep come in 12 combinations
  strdates without a sep can only be an 8-digit stringnumber
  """
  strdatelist = fetch_wordlist_from_textfile_w_filepath(filepath)
  return convert_strdatelist_to_datelist_wo_sep_n_posorder(strdatelist)


def convert_strdatelist_to_datelist_wo_sep_n_posorder(strdatelist):
  try:
    strdatelist = list(strdatelist)
    if len(strdatelist) == 0:
      return []
    datelist = intr.introspect_n_convert_sdlist_to_dates_w_or_wo_sep_n_posorder(strdatelist)
    return list(filter(lambda e: e is not None, datelist))
  except TypeError:
    pass
  return []


def convert_strdatelist_to_datelist_w_sep_n_posorder(strdatelist, sep='-', posorder='ymd'):
  if strdatelist is None or len(strdatelist) == 0:
    return []
  outdatelist = []
  for strdate in strdatelist:
    pdate = intr.convert_strdate_to_date_or_none_w_sep_n_posorder(strdate, sep, posorder)
    if pdate:
      outdatelist.append(pdate)
  return list(filter(lambda e: e is not None, outdatelist))


def fetch_dates_from_strdates_intext_from_filepath_finding_sep_n_posorder(filepath=None):
  strdatelist = fetch_wordlist_from_textfile_w_filepath(filepath)
  sep, posorder = intr.find_sep_n_posorder_from_a_strdatelist(strdatelist)
  if sep and posorder:
    return fetch_dates_w_strdates_sep_n_posorder(strdatelist, sep, posorder)
  return []


def fetch_dates_from_strdates_intext_from_filepath_w_sep_n_posorder(filepath=None, sep='/', posorder='dmy'):
  strdatelist = fetch_wordlist_from_textfile_w_filepath(filepath)
  return fetch_dates_w_strdates_sep_n_posorder(strdatelist, sep, posorder)


def fetch_dates_w_strdates_sep_n_posorder(strdates, sep='/', posorder='dmy'):
  """
  This function extracts dates from files but dates must conform to sep & posorder
  @see other functions in this module that extracts dates under other ways

  strdates with sep & posorder come in 12 different combinations
  strdates without a sep can only be an 8-digit stringnumber

  # notice that dates may be in some different formats (eg "2021-01-21" or "21/1/2021")
  # among these strdates, those that return as "datetime.date" go into datelist
  """
  datelist = map(lambda sd: intr.trans_strdate_from_one_format_to_another_w_sep_n_posorder(sd, sep, posorder), strdates)
  datelist = sorted(filter(lambda e: e is not None, datelist))
  return sorted(datelist)


def form_new_datesfilepath_w_folderpath_n_filename(p_filename=None, p_folderpath=None, followsuffix=True):
  filepath = form_datesfilepath_w_folderpath_n_filename(p_filename, p_folderpath)
  if os.path.exists(filepath):
    if not followsuffix:
      error_msg = f"""Output file {p_filename} already exists in folder:
      => [{p_folderpath}]
      Please, remove it or, programatically, set parameter followsuffix."""
      raise OSError(error_msg)
    else:
      fn_incrementor = sfx_incr.SufixIncrementor(filepath)
      filepath = fn_incrementor.get_next_available_filepath_from_objsparams()
  return filepath


def form_datesfilepath_w_folderpath_n_filename(p_filename=None, p_folderpath=None):
  """
  Forms filepath with folderpath & filename
  """
  folderpath = p_folderpath or sett.get_datafolder_abspath()
  filename = p_filename or DEFAULT_TXT_INPUT_DATES_FILENAME
  if not os.path.exists(folderpath):
    os.makedirs(folderpath)
  filepath = os.path.join(folderpath, filename)
  return filepath


def form_default_datesfilepath():
  return form_datesfilepath_w_folderpath_n_filename(None, None)


def form_default_inputdatesfilepath():
  return form_datesfilepath_w_folderpath_n_filename(DEFAULT_TXT_INPUT_DATES_FILENAME, None)


def get_appsroot_abspath_for_filename_w_tstamp(filename):
  strdt = make_tstamp_for_filename()
  name, ext = os.path.splitext(filename)
  if name.find(' ') > -1:
    filename = name + ' ' + strdt + ext
    filename.replace('  ', ' ')
  else:
    filename = name + '_' + strdt + ext
  return sett.get_appsroot_abspath_for_filename(filename)


def save_without_existence_check_text_to_file(text, output_filepath):
  fd = open(output_filepath, 'w', encoding='utf-8')
  fd.write(text)
  fd.close()
  return output_filepath


def make_tstamp_for_filename(dtime=None):
  if dtime is None or isinstance(dtime, datetime.datetime):
    dtime = datetime.datetime.now()
  strdt = str(dtime)
  strdt = strdt.split('.')[0]
  strdt = strdt.replace(':', '')
  strdt = strdt.replace('-', '')
  strdt = strdt.replace(' ', 'T')
  return strdt


def transform_strdatelist_to_datelist_excl_nones(strdatelist):
  outlist = map(lambda sd: cnv.make_date_or_none(sd), strdatelist)
  return list(filter(lambda d: d is not None, outlist))


def save_without_existence_check_genarator_to_file(genfunc, output_filepath):
  fd = open(output_filepath, 'w', encoding='utf-8')
  n_lines = 0
  for word in genfunc():
    line = f"{str(word)}\n"
    n_lines += 1
    fd.write(line)
  fd.close()
  return n_lines


def adhoc_test1():
  expect_datelist, strdatelist = [], []
  # strdate 1
  y, m, d = 2023, 11, 11
  strdate = f'{y}-{m}-{d}'
  strdatelist.append(strdate)
  pdate = datetime.date(year=y, month=m, day=d)
  expect_datelist.append(pdate)
  # strdate 2
  y, m, d = 2022, 12, 13
  strdate = f'{y}-{m}-{d}'
  strdatelist.append(strdate)
  pdate = datetime.date(year=y, month=m, day=d)
  expect_datelist.append(pdate)
  returned_datelist = convert_strdatelist_to_datelist_w_sep_n_posorder(strdatelist, sep='-', posorder='ymd')
  print('strdatelist', strdatelist, 'expect_datelist', expect_datelist)
  print('returned_datelist', returned_datelist)
  filename = 'testfile.txt'
  fp = make_new_datetimestampsufix_fp_in_configdatafolder_giving_fn(filename)
  print('fp of ', filename, ' => ', fp)
  res = fetch_wordlist_from_textfile_w_filepath()
  print('fetch_wordlist_from_textfile_w_filepath => ', res)


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test1()
